var board = null
var game = new Chess()
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')
var playerColor = 'w' // Player plays White by default

function onDragStart(source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for the side to move
  if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
    (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false
  }

  // only pick up pieces for the player's color
  if (game.turn() !== playerColor) {
    return false
  }
}

function onDrop(source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'

  updateStatus()

  // Make AI move
  window.setTimeout(makeAIMove, 250)
}

function makeAIMove() {
  var difficulty = $('#difficulty').val();
  $.ajax({
    url: '/move',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
      fen: game.fen(),
      difficulty: difficulty
    }),
    success: function (response) {
      if (response.move) {
        console.log("AI move received:", response.move);
        // Parse UCI (e.g. "e2e4", "a7a8q")
        var from = response.move.substring(0, 2);
        var to = response.move.substring(2, 4);
        var promotion = response.move.length > 4 ? response.move.substring(4, 5) : 'q';

        var moveResult = game.move({
          from: from,
          to: to,
          promotion: promotion
        });

        if (moveResult === null) {
          console.error("Illegal move attempted by AI:", response.move);
          alert("AI attempted illegal move: " + response.move);
        }

        board.position(game.fen())
        updateStatus()
      } else if (response.game_over) {
        alert("Game Over! Result: " + response.result)
      }
    },
    error: function (error) {
      console.log("Error:", error)
      alert("AI Error: Check console for details")
    }
  });
}

function onSnapEnd() {
  board.position(game.fen())
}

function updateStatus() {
  var status = ''

  var moveColor = 'White'
  if (game.turn() === 'b') {
    moveColor = 'Black'
  }

  if (game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.'
  } else if (game.in_draw()) {
    status = 'Game over, drawn position'
  } else {
    status = moveColor + ' to move'
    if (game.in_check()) {
      status += ', ' + moveColor + ' is in check'
    }
  }

  $status.html(status)
  updateMoveHistory();
}

function updateMoveHistory() {
  var history = game.history({ verbose: true });
  var html = '';

  for (var i = 0; i < history.length; i += 2) {
    var moveNum = (i / 2) + 1;
    var whiteMove = history[i];
    var blackMove = history[i + 1];

    html += '<div class="move-row">';
    html += '<span class="move-num">' + moveNum + '.</span>';

    // White move
    html += '<span class="move-white" onclick="showPosition(' + i + ')">' + whiteMove.san + '</span>';

    // Black move (if exists)
    if (blackMove) {
      html += '<span class="move-black" onclick="showPosition(' + (i + 1) + ')">' + blackMove.san + '</span>';
    }

    html += '</div>';
  }

  $('#move-history').html(html);

  // Auto-scroll to bottom
  var historyDiv = document.getElementById('move-history');
  if (historyDiv) {
    historyDiv.scrollTop = historyDiv.scrollHeight;
  }
}

// Global function to show position from history
window.showPosition = function (moveIndex) {
  // Create a temporary game to replay moves up to moveIndex
  var tempGame = new Chess();
  var history = game.history();

  for (var i = 0; i <= moveIndex; i++) {
    tempGame.move(history[i]);
  }

  board.position(tempGame.fen());
};

$(document).ready(function () {
  console.log("Document ready!");
  var config = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,
    pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png'
  }

  try {
    console.log("Initializing board...");
    board = Chessboard('board', config)
    console.log("Board initialized:", board);
    updateStatus()

    $(window).resize(board.resize)
  } catch (e) {
    console.error("Error initializing chessboard:", e);
    alert("Error initializing board: " + e);
  }

  $('#resetBtn').on('click', function () {
    console.log("Reset clicked");
    game.reset()
    board.start()
    playerColor = 'w'; // Reset to White
    updateStatus()
  })

  $('#flipBtn').on('click', function () {
    console.log("Flip clicked");
    board.flip();

    // Toggle player color
    playerColor = (playerColor === 'w') ? 'b' : 'w';
    console.log("Player is now playing as:", playerColor === 'w' ? "White" : "Black");

    // If it's now AI's turn (AI plays opposite of playerColor), make a move
    if (game.turn() !== playerColor) {
      window.setTimeout(makeAIMove, 250);
    }
  })
});
