let url = window.location.href
let arr = url.split("/");
let result = arr[0] + "//" + arr[2] + "/pegarendereco/"
$("#cep").focusout(function () {
    $.ajax({
        url: result + $(this).val(),
        dataType: 'json',
        success: function (resposta) {
            $("#logradouro").val(resposta.logradouro);
            //$("#complemento").val(resposta.complemento);
            $("#bairro").val(resposta.bairro);
            $("#cidade").val(resposta.localidade);
            $("#uf").val(resposta.uf);
            $("#complemento").focus();
        }
    });
});