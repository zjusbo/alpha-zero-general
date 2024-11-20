import os
import sys
import time
import copy

import numpy as np
import logging
from tqdm import tqdm

sys.path.append('../../')
from utils import *
from NeuralNet import NeuralNet

import torch
import torch.optim as optim
import torch.utils.benchmark as benchmark

from .GomokuNNet import GomokuNNet as gonet

log = logging.getLogger(__name__)

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'mps': torch.backends.mps.is_available(),
    'num_channels': 512,
    'input_channels': 2,
})


class NNetWrapper(NeuralNet):
    def __init__(self, game, input_channels = 2):
        self.args = copy.copy(args)
        self.args.input_channels = input_channels
        print(f"input_channels: {self.args.input_channels}")
        self.nnet = gonet(game, self.args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        if args.cuda:
            self.nnet.cuda()
        elif args.mps:
            self.nnet = self.nnet.to('mps')

    def train(self, examples, preload_data_for_gpu = True):
        """
        examples: list of examples, each example is of form (board, pi, v)
        preload_data_for_gpu: preload examples on GPU memory. It can speed up training but might blow the GPU memory. 
            Disable it if you encounter any 
        """
        optimizer = optim.Adam(self.nnet.parameters())
        # if args.mps and preload_data_for_gpu:
        #     # move input to MPS
        #     examples = []

        for epoch in range(args.epochs):
            print('EPOCH ::: ' + str(epoch + 1))
            self.nnet.train()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()

            batch_count = len(examples) // args.batch_size
            t = tqdm(range(batch_count), desc='Training Net')
            for _ in t:
                sample_ids = np.random.randint(len(examples), size=args.batch_size)
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))

                boards = np.array(boards)
                black_stones = (boards == 1).astype(np.float32)
                white_stones = (boards == -1).astype(np.float32)
                boards = np.stack([black_stones, white_stones], axis=1)  # Shape: (batch_size, 2, board_x, board_y)
                boards = torch.FloatTensor(boards)
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float32))

                # predict
                if args.cuda:
                    boards, target_pis, target_vs = boards.contiguous().cuda(), target_pis.contiguous().cuda(), target_vs.contiguous().cuda()
                elif args.mps:
                    boards, target_pis, target_vs = boards.contiguous().to('mps'), target_pis.contiguous().to('mps'), target_vs.contiguous().to('mps')
                # compute output
                out_pi, out_v = self.nnet(boards)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                # record loss
                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))
                t.set_postfix(Loss_pi=pi_losses, Loss_v=v_losses)

                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        # Preprocess the board into two channels
        # TODO: optimize it. move it to MPS first? then convert.
        if self.args.input_channels == 2:
            black_stones = (board == 1).astype(np.float32)
            white_stones = (board == -1).astype(np.float32)
            board = np.stack([black_stones, white_stones], axis=0)  # Shape: (2, board_x, board_y)
        
        board = torch.FloatTensor(board.astype(np.float32))
        if args.cuda: board = board.contiguous().cuda()
        elif args.mps: board = board.contiguous().to('mps') 
        board = board.view(self.args.input_channels, self.board_x, self.board_y)
        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(board)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]

    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs) / targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save({
            'state_dict': self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise ("No model in path {}".format(filepath))
        map_location = None 
        if args.cuda:
            map_location = 'cuda'
        elif args.mps:
            map_location = 'mps'
        else:
            map_location = 'cpu'
        checkpoint = torch.load(filepath, map_location=map_location)
        self.nnet.load_state_dict(checkpoint['state_dict'])