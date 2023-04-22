"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $submitForm = $("#newWordForm");


let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  for (let y = 0; y < board.length; y++) {
    let $trow = $("<tr>");

    for (let x = 0; x < board[y].length; x++) {
      let $tcell = $("<td>");
      $tcell.text(board[y][x]);
      $trow.append($tcell);
    }

    $table.append($trow)
  }
}

async function handleFormSubmit(evt) {
  evt.preventDefault();

  let $wordInput = $("#wordInput");

  let $word = $wordInput.val().toUpperCase();

  const response = await axios.request(
    {
      method: 'POST',
      url: 'http://localhost:5001/api/score-word',
      headers: {'Content-Type': 'application/json'},
      data: {gameId: gameId, word: $word}
    }
  )

  let result = response.data.result;

  legalPlay(result, $word);

  $wordInput.val("");

}

$submitForm.on("submit", handleFormSubmit);

function legalPlay(result, word) {
  $message.text("");

  if (result === "ok") {
    let $newWord = $(`<li>${word}</li>`);
    $playedWords.append($newWord);
  } else {
    $message.text(`This word is ${result}`)
  }
}


start();