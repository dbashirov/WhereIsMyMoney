function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setType() {
    let sUrl = window.location.search;
    if(sUrl.indexOf('addIncome') + 1) {
        id_type.value = 'Доход';
    }
}


// События 
window.onload = function () {
    setType()
    updateSelect();
}

id_type.onchange = function () {
    updateSelect();
};

id_wallet.onchange = function () {
    updateSelect();
};


function updateSelect() {

    if (id_type.value == 'Перевод') {

        document.getElementById('div_id_category').style.display = 'none'
        document.getElementById('div_id_wallet_recipient').style.display = 'block'
        // document.getElementById('div_id_category').hidden = true
        // document.getElementById('div_id_wallet_recipient').hidden = false

        // Чистим все категории
        let categorySelect = document.getElementById('id_category');
        while (categorySelect.firstChild) {
            categorySelect.removeChild(categorySelect.firstChild);
        }
        
        updateSelectWalletRecipinet();

    } else {

        document.getElementById('div_id_category').style.display = 'block'
        document.getElementById('div_id_wallet_recipient').style.display = 'none'

        // Чистим все получатели
        let walletSelect = document.getElementById('id_wallet_recipient');
        while (walletSelect.firstChild) {
            walletSelect.removeChild(walletSelect.firstChild);
        }

        updateSelectCategory();

    }
}

function updateSelectWalletRecipinet() {

    // console.log("Start");
    // console.log(id_wallet.value);
    if (id_wallet.value == undefined) {
        return;
    }
    data = JSON.stringify({
        wallet: id_wallet.value
    });
    url = "wallet_recipient-ajax/";

    // Отправка запроса на сервер
    let response = fetch(url, {
        method: "POST",
        body: data,
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie('csrftoken'),
        }
    })
        .then(response => response.json())
        .then(data => {

            // Костыль
            let walletRecipientSelect = document.getElementById('id_wallet_recipient');

            // Сохраняем предыдующий элемент
            prevValue = walletRecipientSelect.value;

            //  Сначала все чистим
            while (walletRecipientSelect.firstChild) {
                walletRecipientSelect.removeChild(walletRecipientSelect.firstChild);
            }

            // Добавляем пустую строку
            walletRecipientSelect.appendChild(new Option("---------"));

            for (let key in data) {
                let walletOption = document.createElement('option');
                walletOption.value = data[key].id;
                walletOption.innerHTML = data[key].title;
                walletRecipientSelect.appendChild(new Option(data[key].title, data[key].id));
                if (prevValue === walletOption.value) {
                    walletRecipientSelect.lastChild.selected = true;
                }
            }
        });
}


function updateSelectCategory() {

    data = JSON.stringify({
        type: id_type.value
    })
    url = "category-ajax/";

    // Отправка запроса на сервер
    let response = fetch(url, {
        method: "POST",
        body: data,
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie('csrftoken'),
        }
    })
        .then(response => response.json())
        .then(data => {

            // Костыль
            let categorySelect = document.getElementById('id_category');

            // Сохраняем предыдующий элемент
            prevValue = categorySelect.value;

            //  Сначала все чистим
            while (categorySelect.firstChild) {
                categorySelect.removeChild(categorySelect.firstChild);
            }

            // Добавляем пустую строку
            // let categoryOption = document.createElement('option');
            // categoryOption.innerHTML = "---------";
            categorySelect.appendChild(new Option("---------"));

            for (let key in data) {
                let categoryOption = document.createElement('option');
                categoryOption.value = data[key].id;
                categoryOption.innerHTML = data[key].title;
                categorySelect.appendChild(categoryOption);
                if (prevValue === categoryOption.value) {
                    categorySelect.lastChild.selected = true;
                }
            }
        });
}


