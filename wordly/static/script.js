// импортируем слова из файла
import { FOUR_WORDS } from "./four_words.js";
import { FIVE_WORDS } from "./five_words.js";
import { SIX_WORDS } from "./six_words.js";

const NUMBER_OF_GUESSES = 5;
let guessesRemaining = [NUMBER_OF_GUESSES, NUMBER_OF_GUESSES];
let currentGuess = [];
let nextLetter = 0;

let p0_words = JSON.parse(document.getElementById('p0_words').textContent);
let p1_words = JSON.parse(document.getElementById('p1_words').textContent);
let words = [p0_words.split(";"), p1_words.split(";")]
let letters = JSON.parse(document.getElementById('letters').textContent);
let now_player = JSON.parse(document.getElementById('now_player').textContent);
let other_player = Number((!Boolean(now_player)))
let winner = JSON.parse(document.getElementById('winner').textContent);
let winword = JSON.parse(document.getElementById('winword').textContent);
let disable = false
let now_player_board = "letter-row_" + String(now_player)
let other_player_board = "letter-row_" + String(other_player)

function color_letter(box, now_color, tips_letter) {
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
}

// создаём игровое поле
function initBoard() {
    // 2 секции - 2 игрока
    for (let j = 0; j < 2; j++) {
        let section = document.createElement("section")
        section.id = "player_" + (j + 1)
        document.getElementById("game-board").appendChild(section)
        let h2 = document.createElement("h2")
        h2.textContent = "Player " + (j + 1)
        section.appendChild(h2)
        // 5 строк - 5 слов
        for (let i = 0; i < NUMBER_OF_GUESSES; i++) {
            let row = document.createElement("div")
            row.className = "letter-row_" + (j)
            // 4-6 букв
            for (let g = 0; g < letters; g++) {
                let box = document.createElement("div")
                box.className = "letter-box"
                if (words[j][0] != "" && words[j].length - 1 > i) {
                    let now_word = words[j][i].split(",")
                    let tips_letter = document.getElementsByName(now_word[g][0])[0]
                    color_letter(box, now_word[g][2], tips_letter)
                    box.textContent = now_word[g][0]
                }
                row.appendChild(box)
            }
            if (words[j].length - 1 > i) {
                guessesRemaining[j] -= 1
            }
            section.appendChild(row)
        }
    }
    // подсвечиваем зеленым фоном чей сейчас ход
    if (guessesRemaining[0] === guessesRemaining[1] && !winner) {
        document.getElementById("player_2").className = 'now_turn'
    }
    if (guessesRemaining[0] > guessesRemaining[1] && !winner) {
        document.getElementById("player_1").className = 'now_turn'
    }
    // если конец - выводим ссылку
    if (winner) {
        let link = document.createElement("a")
        link.appendChild(document.createTextNode("Вернуться в создание и поиск лобби"))
        let lobby_url = document.URL.split('/')
        link.href = lobby_url[0] + '/' + lobby_url[1] + '/' + lobby_url[2] + '/' + lobby_url[3] + '/' + lobby_url[4]
        link.className = "return"
        document.body.appendChild(link)
    }
}
// закончена ли игра
function checkEnd() {
    if (winner) {
        if (winner != "0") {
            let winner_h2 = document.createElement("h2")
            winner_h2.textContent = "Победитель!"
            document.getElementById("Player_" + winner).appendChild(winner_h2)
        } else {
            let first_row_keyboard = document.getElementById('first')
            let winner_h2 = document.createElement("h2")
            winner_h2.textContent = "Никто не отгадал слово |" + winword + "|"
            first_row_keyboard.parentNode.insertBefore(winner_h2, first_row_keyboard)
        }
        disable = true
    }
}

// обновляем доску при получении новых данных
function update_board(json_data, player_update) {
    if (json_data['post'] != false) {
        if (player_update === 2) {
            // обновление своей доски, после отправки слова
            var row = document.getElementsByClassName(now_player_board)[NUMBER_OF_GUESSES - guessesRemaining[now_player]]
            var word = json_data['p' + String(now_player) + '_words'].split(";")[NUMBER_OF_GUESSES - guessesRemaining[now_player]]
            guessesRemaining[now_player] -= 1
        } else {
            // обновление чужой доски, при получении новых данных
            var row = document.getElementsByClassName(other_player_board)[NUMBER_OF_GUESSES - guessesRemaining[other_player]]
            var word = json_data['p' + String(other_player) + '_words'].split(";")[NUMBER_OF_GUESSES - guessesRemaining[other_player]]
            guessesRemaining[other_player] -= 1
        }
        for (let g = 0; g < letters; g++) {
            let box = row.children[g]
            let now_word = word.split(",")
            let tips_letter = document.getElementsByName(now_word[g][0])[0]
            color_letter(box, now_word[g][2], tips_letter)
            box.textContent = now_word[g][0]
        }
        p0_words, p1_words, winner = json_data['p0_words'], json_data['p0_words'], json_data['winner']
        nextLetter, currentGuess = 0, []
        if (guessesRemaining[0] === guessesRemaining[1] && !winner) {
            document.getElementsByClassName("now_turn")[0].className = ''
            document.getElementById("player_2").className = 'now_turn'
        }
        if (guessesRemaining[0] > guessesRemaining[1] && !winner) {
            document.getElementsByClassName("now_turn")[0].className = ''
            document.getElementById("player_1").className = 'now_turn'
        }
    }
}


// отправляем запрос на сервер
function json_request(method, guessString = false) {
    let http = new XMLHttpRequest()
    http.open(method, document.URL + 'l' + 'q');
    if (method === "GET") {
        http.onload = () => {
            if (http.status == 200) {
                let json = http.response;
                if (json['p0_words'] != p0_words ||
                    json['p1_words'] != p1_words ||
                    json['winner']) {
                    update_board(json, 1)
                }
            }
        };
        http.responseType = "json";
        http.setRequestHeader("Accept", "application/json")
        http.send()

    }
    if (method === "POST") {
        const NAME = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';')
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, NAME.length + 1) === (NAME + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(NAME.length + 1));
                    break;
                }
            }
        }
        http.onreadystatechange = function () {
            if (http.readyState === 4 && http.status === 200) {
                update_board(JSON.parse(http.responseText), 2)
                setTimeout(wait_other, 1000)
            }
        }
        http.setRequestHeader('X-CSRFToken', cookieValue);
        http.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        http.send(JSON.stringify({ "guess_word": guessString }));
    }
}

// проверка введённого слова
function checkGuess() {
    let guessString = ''

    for (const val of currentGuess) {
        guessString += val.toLowerCase()
    }

    if (guessString.length != letters) {
        toastr.error("Введены не все буквы!");
        return;
    }
    let WORDS_DICT = ''
    if (letters === 4) { WORDS_DICT = FOUR_WORDS }
    if (letters === 5) { WORDS_DICT = FIVE_WORDS }
    if (letters === 6) { WORDS_DICT = SIX_WORDS }
    if (!WORDS_DICT.includes(guessString)) {
        toastr.error("Такого слова нет в списке!")
        return;
    }

    // после проверки существования слова - отправка на сервер
    json_request("POST", guessString)
}

// удаление символа
function deleteLetter() {
    let box = document.getElementsByClassName(now_player_board)[NUMBER_OF_GUESSES - guessesRemaining[now_player]].children[nextLetter - 1]
    box.textContent = ""
    box.classList.remove("filled-box")
    currentGuess.pop()
    nextLetter -= 1
}

// выводим букву в клетку
function insertLetter(pressedKey) {
    if (nextLetter === letters) {
        return;
    }
    let box = document.getElementsByClassName(now_player_board)[NUMBER_OF_GUESSES - guessesRemaining[now_player]].children[nextLetter]
    box.textContent = pressedKey
    box.classList.add("filled-box")
    currentGuess.push(pressedKey)
    nextLetter += 1
}

// обработчик нажатия на клавиши
document.addEventListener("keydown", (e) => {
    if (disable) {
        // если игра выйграна, нет смысла играть дальше
        if (!document.getElementById('toast-container')) {
            toastr.error("Игра окончена!")
        }
        return
    }
    if (now_player == 0 && guessesRemaining[0] === guessesRemaining[1]) {
        if (!document.getElementById('toast-container')) {
            toastr.error("Ход 2-ого игрока!")
        }
        return
    }
    if (now_player == 1 && guessesRemaining[0] > guessesRemaining[1]) {
        if (!document.getElementById('toast-container')) {
            toastr.error("Ход 1-ого игрока!")
        }
        return
    }

    let pressedKey = String(e.key)
    if (pressedKey === "Backspace") {
        if (nextLetter !== 0) {
            deleteLetter();
            return;
        } else {
            return
        }

    }

    if (pressedKey === "Enter") {
        checkGuess();
        return;
    }

    let found = pressedKey.match(/[а-ё]/gi)
    if (!found || found.length > 1) {
        toastr.error("Только русские буквы из русской раскладки!")
        return
    } else {
        insertLetter(pressedKey)
    }

})

// создание поля при загрузке
initBoard();
// проверка окончания игры
checkEnd();
// при окончании игры, обновления страницы не будет
if (!winner) {
    wait_other()
}
function wait_other() {
    // пока ход другого игрока - страница обновляется каждую секунду
    if ((now_player == 0 && guessesRemaining[0] === guessesRemaining[1]) || (now_player == 1 && guessesRemaining[0] > guessesRemaining[1])) {
        json_request("GET")
        setTimeout(wait_other, 1000)
    } else {
        toastr.success("Ваш ход!")
    }
}