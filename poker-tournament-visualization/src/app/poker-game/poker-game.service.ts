import { Injectable } from '@angular/core';


export interface Player {
  cards: string[];
  name: string;
  total_reward: number;
  winner?: boolean;
}

export interface PokerGame {
  game_nbr: number;
  tournament_stage: string;
  player1: TopLevelPlayer1;
  player2: TopLevelPlayer1;
  hands: Hand[];
  winner?: string;
}

export interface Hand {
  nbr: number;
  raise_count: number;
  abs_reward: number;
  player1: HandPlayer1;
  player2: HandPlayer1;
  history: History[];
  player1_total_reward_before?: number;
  player2_total_reward_before?: number;
  winner?: string;
}

export interface History {
  player?: string;
  action: string;
  stage_contribution?: number;
  stack?: number;
  pot?: number;
  board_cards?: string[];
  player1_hand_type?: string;
  player2_hand_type?: string;
}

export interface HandPlayer1 {
  total_reward_before: number;
  winner: boolean;
  cards: string[];
}

export interface TopLevelPlayer1 {
  name: string;
  total_reward: number;
  winner?: boolean;
}

export interface PlayerState {
  chips_wagered: number;
  stack: number;
  next_to_act: boolean;
  action: string;
}

export enum Stage {
  Preflop = "PREFLOP",
  Flop = "FLOP",
  Turn = "TURN",
  River = "RIVER",
  Showdown = "SHOWDOWN"
}

@Injectable({
  providedIn: 'root'
})
export class PokerGameService {
  game: PokerGame[];

  constructor() {
    this.game = [
      {
        "hands": [
          {
            "player1": {
              "total_reward_before": 0,
              "cards": [
                "6c",
                "2h"
              ],
              "winner": false
            },
            "player2": {
              "total_reward_before": 0,
              "cards": [
                "Qd",
                "5c"
              ],
              "winner": true
            },
            "history": [
              {
                "player": "player1",
                "action": "small_blind",
                "stage_contribution": 5,
                "stack": 995
              },
              {
                "player": "player2",
                "action": "big_blind",
                "stage_contribution": 10,
                "stack": 990
              },
              {
                "player": "player1",
                "action": "FOLD",
                "stage_contribution": 5,
                "stack": 995
              },
              {
                "action": "END_HIDDEN",
                "board_cards": [],
                "pot": 15
              }
            ],
            "nbr": 1,
            "raise_count": 0,
            "abs_reward": 5
          },
          {
            "player1": {
              "total_reward_before": -5,
              "cards": [
                "2d",
                "Ac"
              ],
              "winner": false
            },
            "player2": {
              "total_reward_before": 5,
              "cards": [
                "Qd",
                "6d"
              ],
              "winner": true
            },
            "history": [
              {
                "player": "player2",
                "action": "small_blind",
                "stage_contribution": 5,
                "stack": 995
              },
              {
                "player": "player1",
                "action": "big_blind",
                "stage_contribution": 10,
                "stack": 990
              },
              {
                "player": "player2",
                "action": "RAISE",
                "stage_contribution": 20,
                "stack": 980
              },
              {
                "player": "player1",
                "action": "RAISE",
                "stage_contribution": 30,
                "stack": 970
              },
              {
                "player": "player2",
                "action": "CALL",
                "stage_contribution": 30,
                "stack": 970
              },
              {
                "action": "FLOP",
                "board_cards": [
                  "9s",
                  "5d",
                  "Ah"
                ],
                "pot": 60
              },
              {
                "player": "player2",
                "action": "RAISE",
                "stage_contribution": 10,
                "stack": 960
              },
              {
                "player": "player1",
                "action": "RAISE",
                "stage_contribution": 20,
                "stack": 950
              },
              {
                "player": "player2",
                "action": "CALL",
                "stage_contribution": 20,
                "stack": 950
              },
              {
                "action": "TURN",
                "board_cards": [
                  "9s",
                  "5d",
                  "Ah",
                  "6s"
                ],
                "pot": 100
              },
              {
                "player": "player2",
                "action": "RAISE",
                "stage_contribution": 20,
                "stack": 930
              },
              {
                "player": "player1",
                "action": "RAISE",
                "stage_contribution": 40,
                "stack": 910
              },
              {
                "player": "player2",
                "action": "CALL",
                "stage_contribution": 40,
                "stack": 910
              },
              {
                "action": "RIVER",
                "board_cards": [
                  "9s",
                  "5d",
                  "Ah",
                  "6s",
                  "6c"
                ],
                "pot": 180
              },
              {
                "player": "player2",
                "action": "RAISE",
                "stage_contribution": 20,
                "stack": 890
              },
              {
                "player": "player1",
                "action": "RAISE",
                "stage_contribution": 40,
                "stack": 870
              },
              {
                "player": "player2",
                "action": "CALL",
                "stage_contribution": 40,
                "stack": 870
              },
              {
                "action": "SHOWDOWN",
                "board_cards": [
                  "9s",
                  "5d",
                  "Ah",
                  "6s",
                  "6c"
                ],
                "pot": 260,
                "player1_hand_type": "TWOPAIR",
                "player2_hand_type": "THREEOFAKIND"
              }
            ],
            "nbr": 2,
            "raise_count": 8,
            "abs_reward": 130
          },
          {
            "player1": {
              "total_reward_before": -135,
              "cards": [
                "8d",
                "3h"
              ],
              "winner": false
            },
            "player2": {
              "total_reward_before": 135,
              "cards": [
                "Qs",
                "9h"
              ],
              "winner": true
            },
            "history": [
              {
                "player": "player1",
                "action": "small_blind",
                "stage_contribution": 5,
                "stack": 995
              },
              {
                "player": "player2",
                "action": "big_blind",
                "stage_contribution": 10,
                "stack": 990
              },
              {
                "player": "player1",
                "action": "FOLD",
                "stage_contribution": 5,
                "stack": 995
              },
              {
                "action": "END_HIDDEN",
                "board_cards": [],
                "pot": 15
              }
            ],
            "nbr": 3,
            "raise_count": 0,
            "abs_reward": 5
          },
          {
            "player1": {
              "total_reward_before": -140,
              "cards": [
                "5h",
                "3h"
              ],
              "winner": false
            },
            "player2": {
              "total_reward_before": 140,
              "cards": [
                "6s",
                "Ac"
              ],
              "winner": true
            },
            "history": [
              {
                "player": "player2",
                "action": "small_blind",
                "stage_contribution": 5,
                "stack": 995
              },
              {
                "player": "player1",
                "action": "big_blind",
                "stage_contribution": 10,
                "stack": 990
              },
              {
                "player": "player2",
                "action": "RAISE",
                "stage_contribution": 20,
                "stack": 980
              },
              {
                "player": "player1",
                "action": "FOLD",
                "stage_contribution": 10,
                "stack": 990
              },
              {
                "action": "END_HIDDEN",
                "board_cards": [],
                "pot": 30
              }
            ],
            "nbr": 4,
            "raise_count": 1,
            "abs_reward": 10
          }
        ],
        "player1": {
          "name": "Boevle",
          "total_reward": -150,
          "winner": false
        },
        "player2": {
          "name": "Harder",
          "total_reward": 150,
          "winner": true
        },
        "game_nbr": 1,
        "tournament_stage": "quaters"
      }
    ]
  }
}
