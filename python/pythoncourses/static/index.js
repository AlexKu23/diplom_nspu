// Запрос на сервер
function jx(method, url, headers, data, def) {
    const request = new XMLHttpRequest();
    request.open(method, url);
    for (let key in headers) {
        request.setRequestHeader(key, headers[key]);
    }
    request.send(data);

    request.addEventListener('readystatechange', function () {
        if (request.readyState === 4 && request.status === 200) {
            def(JSON.parse(request.response));
        }
    });
}

// Получение куки
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

// Заголовки для запроса
const headers = {
    'Content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': getCookie('csrftoken')
};

// Добавление интерактивным примерам редактора и подключение интерпретатора

let editors = [...document.getElementsByClassName('example')];

for (let ed of editors) {
    let codeInEditor = ed.value;
    let dv = document.createElement('div');
    let inp = document.createElement('button');
    let textar = document.createElement('textarea');
    textar.setAttribute('class', 'outp');
    textar.setAttribute('readonly', 'readonly');
    inp.setAttribute('class', 'btn-hover color-10');
    inp.textContent = 'Запустить';
    ed.insertAdjacentElement('beforebegin', inp);
    ed.insertAdjacentElement('afterend', textar);
    ed.insertAdjacentElement('afterend', dv);
    ed.remove();
    const editor = CodeMirror(dv, {
        value: codeInEditor,
        mode: "python",
        indentUnit: 4,
        lineNumbers: true,
        readOnly: true
    });

    inp.onclick = function () {
        function inpPrompt() {
            let inp = window.prompt();
            textar.value = textar.value + inp + '\n';
            return inp;
        }


        function outf(text) {
            textar.value = textar.value + text;
        }

        function builtinRead(x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                throw "File not found: '" + x + "'";
            return Sk.builtinFiles["files"][x];
        }

        function runit(codee) {
            let prog = codee;


            textar.value = '';
            Sk.configure({output: outf, read: builtinRead, inputfun: inpPrompt});
            (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'mycanvas';
            var myPromise = Sk.misceval.asyncToPromise(function () {
                return Sk.importMainWithBody("<stdin>", false, prog, true);
            });
            myPromise.then(function (mod) {
                    textar.style.display = 'block'
                },
                function (err) {
                    textar.style.display = 'block';
                    textar.value = textar.value + err.toString();
                });
        }

        runit(editor.getValue());
    }
}

// Добавление задачам редактора и подключение интерпретатора
editors = document.getElementsByClassName('task');
editors = [...editors];
for (let ed of editors) {
    editorTask = document.createElement('div');
    let dv = document.createElement('div');
    let checkSolution = document.createElement('button');
    let inp = document.createElement('button');
    let textar = document.createElement('textarea');
    let textarTest = document.createElement('textarea');
    textarTest.setAttribute('class', 'outp');
    textarTest.setAttribute('readonly', 'readonly');
    textar.setAttribute('class', 'outp');
    textar.setAttribute('readonly', 'readonly');
    checkSolution.setAttribute('class', 'btn-hover color-7');
    checkSolution.setAttribute('id', ed.id)
    checkSolution.textContent = 'Проверить';
    inp.setAttribute('class', 'btn-hover color-10');
    inp.textContent = 'Запустить';
    editorTask.appendChild(checkSolution);
    editorTask.appendChild(inp);
    editorTask.appendChild(dv);
    editorTask.appendChild(textar);
    editorTask.appendChild(textarTest)
    ed.appendChild(editorTask);
    const editor = CodeMirror(dv, {
        mode: "python",
        indentUnit: 4,
        lineNumbers: true,
        lineWrapping: true

    });

    checkSolution.onclick = function () {
        function testSolution(tests) {
            textarTest.value = '';
            let numberCorrect = 0;
            for (let test of tests.tests) {
                let result = '';

                function readline() {
                    return inputTest.shift()
                }

                function outf(text) {
                    result = result + text;
                }

                function builtinRead(x) {
                    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                        throw "File not found: '" + x + "'";
                    return Sk.builtinFiles["files"][x];
                }

                function runitTest(codee) {
                    let prog = codee;
                    Sk.configure({output: outf, read: builtinRead, inputfun: readline});
                    (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'mycanvas';
                    var myPromise = Sk.misceval.asyncToPromise(function () {
                        return Sk.importMainWithBody("<stdin>", false, prog, true);
                    });
                    myPromise.then(function (mod) {
                            textar.style.display = 'none'
                        },
                        function (err) {
                            result = result + err.toString();
                        });
                }

                let inputTest = test.in.split('\r\n');
                let outputTest = test.out.replaceAll('\r', '') + '\n';

                runitTest(editor.getValue());

                if (outputTest === result) {
                    numberCorrect++;
                } else {
                    textarTest.value = textarTest.value + `Входные данные:\n${test.in}\nОжидалось:\n${outputTest}\nПолучено:\n${result}`;
                }

            }
            let percent = (numberCorrect / tests.tests.length).toFixed(2);

            if (textarTest.previousSibling.tagName === "TEXTAREA") {
                if (percent == 1) {
                    textarTest.insertAdjacentText("beforebegin", 'Все правильно! Молодец! 100%');
                    textarTest.style.display = 'none';

                } else {
                    textarTest.insertAdjacentText('beforebegin', `Пройденных тестов ${percent * 100}%`);
                    textarTest.style.display = 'block';
                }
            } else {
                if (percent == 1) {
                    textarTest.previousSibling.textContent = 'Все правильно! Молодец! 100%';
                    textarTest.style.display = 'none';
                } else {
                    textarTest.previousSibling.textContent = `Пройденных тестов ${percent * 100}%`;
                    textarTest.style.display = 'block';
                }

            }


        }

        const data = `id=${this.id}`;
        jx('POST', document.location.origin + '/task/', headers, data, testSolution);

    };

    inp.onclick = function () {
        function inpPrompt() {
            let inp = window.prompt();
            textar.value = textar.value + inp + '\n';
            return inp;
        }

        function outf(text) {
            textar.value = textar.value + text;
        }

        function builtinRead(x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                throw "File not found: '" + x + "'";
            return Sk.builtinFiles["files"][x];
        }

        function runit(codee) {
            let prog = codee;
            textar.style.display = 'block';
            textar.value = '';
            Sk.configure({output: outf, read: builtinRead, inputfun: inpPrompt});
            (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'mycanvas';
            var myPromise = Sk.misceval.asyncToPromise(function () {
                return Sk.importMainWithBody("<stdin>", false, prog, true);
            });
            myPromise.then(function (mod) {
                    textar.style.display = 'block';
                },
                function (err) {
                    textar.style.display = 'block';
                    textar.value = textar.value + err.toString();
                });
        }

        runit(editor.getValue());
    }
}

// Создание свободного редактора
const ed = document.querySelector('main');
if (ed) {
    const svg = document.querySelector('svg');
    const editor = CodeMirror(ed, {
        mode: "python",
        indentUnit: 4,
        lineNumbers: true
    });

    const textEditor = document.createElement('textarea');
    textEditor.setAttribute('class', 'output');
    ed.appendChild(textEditor);

    svg.onclick = function () {
        function inpPrompt() {
            let inp = window.prompt();
            textEditor.value = textEditor.value + inp + '\n';
            return inp;
        }

        function outf(text) {
            textEditor.value = textEditor.value + text;
        }

        function builtinRead(x) {
            if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                throw "File not found: '" + x + "'";
            return Sk.builtinFiles["files"][x];
        }

        function runit(codee) {
            let prog = codee;
            textEditor.value = '';
            Sk.configure({output: outf, read: builtinRead, inputfun: inpPrompt});
            (Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = 'mycanvas';
            var myPromise = Sk.misceval.asyncToPromise(function () {
                return Sk.importMainWithBody("<stdin>", false, prog, true);
            });
            myPromise.then(function (mod) {
                    textEditor.style.display = 'block';
                },
                function (err) {
                    textar.style.display = 'block';
                    textEditor.value = textEditor.value + err.toString();
                });
        }

        runit(editor.getValue());
    };
}




