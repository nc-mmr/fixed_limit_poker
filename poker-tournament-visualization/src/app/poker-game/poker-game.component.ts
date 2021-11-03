import { Component, OnChanges, OnInit, Output } from '@angular/core';
import { MatSliderChange } from '@angular/material/slider';
import { PokerGame, PokerGameService, Stage, History } from './poker-game.service';

@Component({
  selector: 'app-poker-game',
  templateUrl: './poker-game.component.html',
  styleUrls: ['./poker-game.component.css']
})
export class PokerGameComponent implements OnInit, OnChanges {
  game: PokerGame;
  stage: Stage;
  actionSlider: number = 0;
  hand: number = 0;

  constructor(private pokerGameService: PokerGameService) {
    this.game = this.pokerGameService.game[0];
    this.stage = Stage.Preflop;
  }

  ngOnInit(): void {
    const element = document.getElementById('slider');
    setTimeout(function() { element?.focus() }, 20);    
  }

  ngOnChanges(): void {
    console.log("game changes!")
    this.setStage()
  }

  setStage(val?: number): void {
    const newValue = val ?? this.actionSlider;
    let currentStage = Stage.Preflop;
    for (let index = 0; index <= newValue; index++) {
      const action = this.game.hands[this.hand].history[index].action;
      if (action == Stage.Preflop) {
        currentStage = Stage.Preflop;
      } else if (action == Stage.Flop) {
        currentStage = Stage.Flop;
      } else if (action == Stage.Turn) {
        currentStage = Stage.Turn;
      } else if (action == Stage.River) {
        currentStage = Stage.River;
      } else if (action == Stage.EndHidden) {
        currentStage = Stage.EndHidden;
      }else if (action == Stage.Showdown) {
        currentStage = Stage.Showdown;
      }
    }
    this.stage = currentStage;
  }

  getMaxActions(): number {
    const actions = this.game.hands[this.hand].history.length-1;
    return actions; // +1 for the show-down
  }

  getCurrentAction(): History {
    const idx = this.actionSlider;
    return this.game.hands[this.hand].history[idx];
  }

  sliderOnChange(event: any) {
    this.setStage(event.value)
    this.actionSlider = event.value
  }

  getMaxHands(): number {
    const hands = this.game.hands.length-1;
    return hands; // +1 for the show-down
  }
  handSliderOnChange(event: any) {
    this.hand = event.value;
    this.actionSlider = 0;
    this.setStage(0)
  }
}

