const fetchData = async (url) => {
  const response = await fetch(url);
  console.log(response)

  const data = await response.json();

  return data;
}


const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))


const drawBoard = (view, board) => {
  board.forEach((row, rowIndex) => {
    row.forEach((cell, cellIndex) => {
      const outhterSquareIndex = Math.floor(rowIndex / 3) * 3 + Math.floor(cellIndex / 3);
      const innerSquareIndex = (rowIndex % 3) * 3 + (cellIndex % 3);

      const cellElem = view.children[outhterSquareIndex].querySelector(".outer-square").children[innerSquareIndex].querySelector(".inner-square");

      if (cell != 0) {
        cellElem.innerText = cell;
      }
    });
  });
}


const drawDomains = (view, domains) => {

  domains.forEach((row, rowIndex) => {
    row.forEach((cell, cellIndex) => {
      const outhterSquareIndex = Math.floor(rowIndex / 3) * 3 + Math.floor(cellIndex / 3);
      const innerSquareIndex = (rowIndex % 3) * 3 + (cellIndex % 3);

      const cellElem = view.children[outhterSquareIndex].querySelector(".outer-square").children[innerSquareIndex].querySelector(".inner-square");

      if (cell.length > 0) {
        cellElem.innerHTML = `<div class="center-text">${cell.sort().join("")}</div>`;
      }
    });
  });
}

const handleGameStart = async (e) => {
  try {
    e.preventDefault();
    const form = e.target;
    const view = document.querySelector('#game_board');
    const gameControls = document.querySelector('#game_controls');


    const {
      gameData,
      algorithm,
      stepDelay,
      autoPlay
    } = Object.fromEntries(new FormData(form).entries());

    const gameSolutionData = Object.values(await fetchData(`/Sudoku-solver-project/backend/data/${algorithm}/${gameData.trim()}.json`));

    if (autoPlay === "on") {
      gameControls.querySelectorAll('button').forEach((button) => {
        button.disabled = true;
      });

      for (const step of gameSolutionData) {
        drawBoard(view, step.board);
        drawDomains(view, step.domains);
        await sleep(stepDelay);

      }
    } else {
      const prevButton = gameControls.querySelector('#prev_button');
      const nextButton = gameControls.querySelector('#next_button');

      let stepIndex = 0;
      const drawStep = () => {
        const step = gameSolutionData[stepIndex]
        drawBoard(view, step.board);
        drawDomains(view, step.domains);
      }

      prevButton.addEventListener('click', () => {
        stepIndex = Math.max(0, stepIndex - 1);
        drawStep();
      });

      nextButton.addEventListener('click', () => {
        stepIndex = Math.min(gameSolutionData.length - 1, stepIndex + 1);

        drawStep();
      });

      drawStep();

    }

  } catch (e) {
    alert(e.message);
    console.error(e)
  }
}


const handleGameReset = (e) => {
  e.preventDefault();
  const form = e.target;


}


const main = () => {
  const form = document.querySelector('#game_form');

  form.addEventListener('submit', handleGameStart)
  form.addEventListener('reset', handleGameReset)

}


window.onload = main;