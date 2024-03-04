// импортируем слова из файла
import { FOUR_WORDS } from "./four_words.js";
import { FIVE_WORDS } from "./five_words.js";
import { SIX_WORDS } from "./six_words.js";

const NUMBER_OF_GUESSES = 5;
let guessesRemaining = [NUMBER_OF_GUESSES, NUMBER_OF_GUESSES];
let currentGuess = [];
let nextLetter = 0;
let letters = JSON.parse(document.getElementById('letters').textContent);
let now_player = JSON.parse(document.getElementById('now_player').textContent);
let p1_words = JSON.parse(document.getElementById('p1_words').textContent).split(";");
let p2_words = JSON.parse(document.getElementById('p2_words').textContent).split(";");
let winner = JSON.parse(document.getElementById('winner').textContent);
let words = [p1_words, p2_words]
let tips_letter = ""
let player_board = "letter-row_" + now_player
let now_color = 0
let disable = false


// создаём игровое поле
function initBoard() {
    let board = document.getElementById("game-board");
    for (let j = 0; j < 2; j++) {
        let section = document.createElement("section")
        section.id = "Player_" + (j + 1)
        board.appendChild(section)
        let h2 = document.createElement("h2")
        h2.textContent = "Player " + (j + 1)
        section.appendChild(h2)
        let player_words = words[j]
        for (let i = 0; i < NUMBER_OF_GUESSES; i++) {
            let row = document.createElement("div")
            row.className = "letter-row_" + (j)
            for (let g = 0; g < letters; g++) {
                let box = document.createElement("div")
                box.className = "letter-box"
                if (player_words[0] != "" && player_words.length > i) {
                    let now_word = player_words[i].split(",")
                    now_color = now_word[g][2]
                    tips_letter = document.getElementsByName(now_word[g][0])[0]
                    if (now_color === "0") {
                        box.id = "incorrect"
                        if (tips_letter && tips_letter.id != "correct" && tips_letter.id != "incorrectIndex") {
                            tips_letter.id = "incorrect"
                        }
                    }
                    if (now_color === "1") {
                        box.id = "incorrectIndex"
                        if (tips_letter && tips_letter.id != "correct") {
                            tips_letter.id = "incorrectIndex"
                        }
                    }
                    if (now_color === "2") {
                        box.id = "correct"
                        if (tips_letter) {
                            tips_letter.id = "correct"
                        }
                    }
                    box.textContent = now_word[g][0]
                }
                row.appendChild(box)
            }
            if (player_words[0] != "" && player_words.length > i) {
                guessesRemaining[j] -= 1
            }
            section.appendChild(row)
        }
    }
}

function checkWinner() {
    if (winner != "0") {
        let winner_word = "Player_" + winner
        let winner_section = document.getElementById(winner_word)
        let winner_h2 = document.createElement("h2")
        winner_h2.textContent = "Победитель!"
        winner_section.appendChild(winner_h2)
        disable = true
    }
}

// удаление символа
function deleteLetter() {
    let row = document.getElementsByClassName(player_board)[NUMBER_OF_GUESSES - guessesRemaining[Number(now_player)]]
    let box = row.children[nextLetter - 1]
    box.textContent = ""
    box.classList.remove("filled-box")
    currentGuess.pop()
    nextLetter -= 1
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// проверка введённого слова
function checkGuess() {
    // переменная, где будет наша догадка
    let guessString = ''

    // собираем все введённые в строке буквы в одно слово
    for (const val of currentGuess) {
        guessString += val.toLowerCase()
    }


    // если в догадке меньше 5 букв — выводим уведомление, что букв не хватает
    if (guessString.length != letters) {
        // error означает, что уведомление будет в формате ошибки
        toastr.error("Введены не все буквы!");
        // и после вывода выходим из проверки догадки
        return;
    }
    let WORDS_DICT = ''
    if (letters === 4) { WORDS_DICT = FOUR_WORDS }
    if (letters === 5) { WORDS_DICT = FIVE_WORDS }
    if (letters === 6) { WORDS_DICT = SIX_WORDS }
    if (!WORDS_DICT.includes(guessString)) {
        toastr.error("Такого слова нет в списке!")
        // и после вывода выходим из проверки догадки
        return;
    }

    const post_request = { "guess_word": guessString }
    const Http = new XMLHttpRequest();
    const url = document.URL;
    const csrftoken = getCookie('csrftoken');
    Http.open("POST", url);
    Http.setRequestHeader('X-CSRFToken', csrftoken);
    Http.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    Http.send(JSON.stringify(post_request));
    setTimeout(() => { location.reload(); }, 1000)
}

// выводим букву в клетку
function insertLetter(pressedKey) {
    if (nextLetter === letters) {
        return;
    }
    let row = document.getElementsByClassName(player_board)[NUMBER_OF_GUESSES - guessesRemaining[Number(now_player)]]
    let box = row.children[nextLetter]
    box.textContent = pressedKey
    box.classList.add("filled-box")
    currentGuess.push(pressedKey)
    nextLetter += 1
}

// обработчик нажатия на клавиши
document.addEventListener("keydown", (e) => {
    if (disable) {
        return
    }
    if (now_player == "0" && guessesRemaining[0] === guessesRemaining[1]) {
        toastr.error("Ход другого игрока!")
        return
    }
    if (now_player == "1" && guessesRemaining[0] > guessesRemaining[1]) {
        toastr.error("Ход другого игрока!")
        return
    }

    if (guessesRemaining[Number(now_player)] === 0) {
        return
    }

    let pressedKey = String(e.key)
    if (pressedKey === "Backspace" && nextLetter !== 0) {
        deleteLetter();
        return;
    }

    if (pressedKey === "Enter") {
        checkGuess();
        return;
    }

    let found = pressedKey.match(/[а-ё]/gi)
    if (!found || found.length > 1) {
        return
    } else {
        insertLetter(pressedKey)
    }
})


initBoard();
checkWinner();