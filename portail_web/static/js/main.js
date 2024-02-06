AOS.init();
function sleep(mls) {
    return new Promise((resolve, reject) => setTimeout(resolve, mls))
}


class Custumer {
    constructor(element) {
        this.element = element;
    }
    addClass() {
        this.element.classList.add('d-none');
    }

    removeClass() {
        this.element.classList.remove('d-none');
    }
}

const title = ["Qui somme nous", "Qui est partenaire", "Qui est client"];
const descriptions = ["Nous mettons à la disposition de nos clients les compétences et les talents adaptés à la complexité de leurs environnements techniques.",
    "Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda sunt ducimus rem, reiciendis obcaecati omnis eum asperiores esse eius. Amet, porro quae iusto illo ex accusamus laborum consectetur sunt error? Ratione ad iure quidem veritatis quo rerum omnis vero non similique ipsam odit optio provident iusto assumenda consectetur ipsum ab, veniam sed nobis, sit debitis,",
    "Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda sunt ducimus rem, reiciendis obcaecati omnis eum asperiores esse eius. "];
document.addEventListener('DOMContentLoaded', function () {
    // Formulaire 
    let btnActif = document.querySelector('.btn-toggle');
    const titre = document.getElementById('title');
    const modal = document.getElementById('modal-form');
    const Path = document.getElementById("Path");
    const input = document.querySelectorAll('.form-control');
    const clients = document.querySelectorAll('.client');
    const condidats = document.querySelectorAll('.condidat');
    const secondary = document.getElementById("secondary");
    const main = document.getElementById("main");


    $(".demo1").kwtFileUpload();

    async function printwriter(curWord, typewriterElement) {
        for (let i = 0; i < curWord.length; i++) {
            typewriterElement.innerText = curWord.substring(0, i + 1);
            await sleep(100);
        }
    }
    document.getElementById('showemodal').addEventListener('click', () => {
        const curWord2 = "Votre rÃ©ussite Ã  portÃ©e de main";
        const typewriterElement = document.getElementById('enbleme');
        printwriter(curWord2, typewriterElement);
    });
    const submit = document.getElementById("submit");



    btnActif.addEventListener("click", () => {
        Path.style.transition = "fill 0.2s ease-out";
        if (document.querySelector(".active")) {
            titre.innerText = "Augmentez vos chances d'être contacté par un recruteur";
            modal.style.backgroundColor = "#EEF9FF";
            submit.style.backgroundColor = "#317ACA"
            secondary.style.backgroundColor = "#317ACA";
            Path.setAttribute("fill", "#317ACA");
            for (var i = 0; i < input.length; i++) {
                input[i].style.borderBottom = '1px solid #317ACA';
            };
            console.log(condidats.length);

            for (var i = 0; i < condidats.length; i++) {
                console.log(i);
                console.log(condidats[i]);
                if (condidats[i].classList.contains("d-none")) {
                    condidats[i].classList.remove("d-none");
                    clients[i].classList.add("d-none");
                } else {
                    condidats[i].classList.add("d-none");
                    clients[i].classList.remove("d-none");
                }
            };
        } else {
            titre.innerText = "Recherchez des compÃ©tences et trouvez vos futurs collaborateurs parmi plus de 300 000 profils";
            modal.style.backgroundColor = "#317ACA";
            submit.style.backgroundColor = "#EEF9FF"
            secondary.style.backgroundColor = "#EEF9FF";
            Path.setAttribute("fill", "#EEF9FF");
            for (var i = 0; i < input.length; i++) {
                input[i].style.borderBottom = '1px solid #EEF9FF';
            };
            for (var i = 0; i < clients.length; i++) {
                if (clients[i].classList.contains("d-none")) {
                    clients[i].classList.remove("d-none");
                    condidats[i].classList.add("d-none");
                } else {
                    condidats[i].classList.add("d-none");
                    clients[i].classList.remove("d-none");
                }
            };
        }

    });


    var typewriter = document.getElementById('typewriter');
    var typewriterp = document.getElementById('typewriterp');

    let sleeptime = 100;
    let curTitleIndex = 0;
    let curDescriptionIndex = 0;
    const writeLoop = async () => {
        while (true) {
            let curWord = title[curTitleIndex];
            let curWordDescrption = descriptions[curDescriptionIndex];
            for (let i = 0; i < curWord.length; i++) {
                // typewriter.innertext=curWord.substring(0,i+1);
                typewriter.innerText = curWord.substring(0, i + 1);
                await sleep(sleeptime);
            }
            for (let i = 0; i < curWordDescrption.length; i++) {
                // typewriter.innertext=curWord.substring(0,i+1);
                typewriterp.innerText = curWordDescrption.substring(0, i + 1);
                await sleep(sleeptime / 10);
            }
            await sleep(sleeptime * 120);

            for (let i = curWord.length; i > 0; i--) {
                // typewriter.innertext=curWord.substring(0,i+1);
                typewriter.innerText = curWord.substring(0, i - 1);
                await sleep(sleeptime);
            }
            if (curTitleIndex === title.length - 1) {
                curTitleIndex = 0;
                curDescriptionIndex = 0;
            } else {
                curTitleIndex++;
                curDescriptionIndex++;
            }
            await sleep(sleeptime * 10);
        }
    }

    writeLoop()
});

(function ($) {
    var customDragandDrop = function (element) {
        $(element).addClass("kwt-file__input");
        var element = $(element).wrap(
            `<div class="kwt-file"><div class="kwt-file__drop-area"><span class='kwt-file__choose-file ${element.attributes.data_btn_text
                ? "" === element.attributes.data_btn_text.textContent
                    ? ""
                    : "kwt-file_btn-text"
                : ""
            }'>${element.attributes.data_btn_text
                ? "" === element.attributes.data_btn_text.textContent
                    ? `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor"><path d="M67.508 468.467c-58.005-58.013-58.016-151.92 0-209.943l225.011-225.04c44.643-44.645 117.279-44.645 161.92 0 44.743 44.749 44.753 117.186 0 161.944l-189.465 189.49c-31.41 31.413-82.518 31.412-113.926.001-31.479-31.482-31.49-82.453 0-113.944L311.51 110.491c4.687-4.687 12.286-4.687 16.972 0l16.967 16.971c4.685 4.686 4.685 12.283 0 16.969L184.983 304.917c-12.724 12.724-12.73 33.328 0 46.058 12.696 12.697 33.356 12.699 46.054-.001l189.465-189.489c25.987-25.989 25.994-68.06.001-94.056-25.931-25.934-68.119-25.932-94.049 0l-225.01 225.039c-39.249 39.252-39.258 102.795-.001 142.057 39.285 39.29 102.885 39.287 142.162-.028A739446.174 739446.174 0 0 1 439.497 238.49c4.686-4.687 12.282-4.684 16.969.004l16.967 16.971c4.685 4.686 4.689 12.279.004 16.965a755654.128 755654.128 0 0 0-195.881 195.996c-58.034 58.092-152.004 58.093-210.048.041z" /></svg>`
                    : `${element.attributes.data_btn_text.textContent}`
                : `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor"><path d="M67.508 468.467c-58.005-58.013-58.016-151.92 0-209.943l225.011-225.04c44.643-44.645 117.279-44.645 161.92 0 44.743 44.749 44.753 117.186 0 161.944l-189.465 189.49c-31.41 31.413-82.518 31.412-113.926.001-31.479-31.482-31.49-82.453 0-113.944L311.51 110.491c4.687-4.687 12.286-4.687 16.972 0l16.967 16.971c4.685 4.686 4.685 12.283 0 16.969L184.983 304.917c-12.724 12.724-12.73 33.328 0 46.058 12.696 12.697 33.356 12.699 46.054-.001l189.465-189.489c25.987-25.989 25.994-68.06.001-94.056-25.931-25.934-68.119-25.932-94.049 0l-225.01 225.039c-39.249 39.252-39.258 102.795-.001 142.057 39.285 39.29 102.885 39.287 142.162-.028A739446.174 739446.174 0 0 1 439.497 238.49c4.686-4.687 12.282-4.684 16.969.004l16.967 16.971c4.685 4.686 4.689 12.279.004 16.965a755654.128 755654.128 0 0 0-195.881 195.996c-58.034 58.092-152.004 58.093-210.048.041z" /></svg>`
            }</span>${element.outerHTML}</span><span class="kwt-file__msg">${"" === element.placeholder ? "or drop files here" : `${element.placeholder}`
            }</span><div class="kwt-file__delete"></div></div></div>`
        );
        var element = element.parents(".kwt-file");

        // Add class on focus and drage enter event.
        element.on("dragenter focus click", ".kwt-file__input", function (e) {
            $(this).parents(".kwt-file__drop-area").addClass("is-active");
        });

        // Remove class on blur and drage leave event.
        element.on("dragleave blur drop", ".kwt-file__input", function (e) {
            $(this).parents(".kwt-file__drop-area").removeClass("is-active");
        });

        // Show filename when change file.
        element.on("change", ".kwt-file__input", function (e) {
            let filesCount = $(this)[0].files.length;
            let textContainer = $(this).next(".kwt-file__msg");
            if (1 === filesCount) {
                let fileName = $(this).val().split("\\").pop();
                textContainer
                    .text(fileName)
                    .next(".kwt-file__delete")
                    .css("display", "block");
            } else if (filesCount > 1) {
                textContainer
                    .text(filesCount + " files selected")
                    .next(".kwt-file__delete")
                    .css("display", "inline-block");
            } else {
                textContainer.text(
                    `${"" === this[0].placeholder
                        ? "or drop files here"
                        : `${this[0].placeholder}`
                    }`
                );
                $(this)
                    .parents(".kwt-file")
                    .find(".kwt-file__delete")
                    .css("display", "none");
            }
        });

        // Delete selected file.
        element.on("click", ".kwt-file__delete", function (e) {
            let deleteElement = $(this);
            deleteElement.parents(".kwt-file").find(`.kwt-file__input`).val(null);
            deleteElement
                .css("display", "none")
                .prev(`.kwt-file__msg`)
                .text(
                    `${"" ===
                        $(this).parents(".kwt-file").find(".kwt-file__input")[0].placeholder
                        ? "or drop files here"
                        : `${$(this).parents(".kwt-file").find(".kwt-file__input")[0].placeholder
                        }`
                    }`
                );
        });
    };

    $.fn.kwtFileUpload = function (e) {
        var _this = $(this);
        $.each(_this, function (index, element) {
            customDragandDrop(element);
        });
        return this;
    };
})(jQuery);