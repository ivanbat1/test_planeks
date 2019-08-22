function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})

function submit_form(calbacco, button_id, beforeSubmit, ev) {
    ev.preventDefault();
    console.log(ev);
    if (typeof (beforeSubmit) === 'function') {
        if (!beforeSubmit(ev.target)) {
            return;
        }
    }
    var form = new FormData(ev.target);
    var csrf_cookie;
    for (var keyval of document.cookie.split(";")) {
        if (keyval.includes("csrftoken")) {
            csrf_cookie = keyval.slice(keyval.search("=") + 1);
            break;
        }
    }

    if (csrf_cookie == undefined) {
        console.log("CSRF broke.");
        return false;
    }
    fetch(
        ev.target.action,
        {
            "body": form,
            "method": ev.target.method,
            "headers": {"X-CSRF-TOKEN": csrf_cookie}

        }
    ).then((resp) => {
            return resp.json();
        }
    ).then((rj) => {
        try {
            console.log(rj);
            calbacco(rj);
        } catch (err) {
            console.log("Error in submitForm callback: ", err);
        }
    })
        .catch(function (error) {
            console.log("Probably not json.");
            console.log(error);
            if (button_id == "submitResPass") calbacco(error);
            else alert('forbidden');  // for permissions; searching better solution
        });
    return false;
}


function submitRegistration(data) {
    console.log(data);
    if (data['message']) alert(data['message']);
    if (data['url']) window.location.href = data['url'];
}

function commentJs(data) {
    if (data) document.getElementById('parent').value = data;
    console.log(document.getElementById('parent').value)
}

function subscribe(pk_post) {
    $.ajax({
        url: '/news/',
        type: 'post',
        data: {'pk': pk_post},
        success: function (data) {
            alert(data['message']);
            if (data['message'] === 'add') document.getElementById('subscribe_'+pk_post).innerHTML = 'unsubscribe';
            else document.getElementById('subscribe_'+pk_post).innerHTML = 'subscribe'
        }

    })
}