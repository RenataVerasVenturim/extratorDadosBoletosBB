//------------------------------------------------------------------------notas fiscais
document.addEventListener('DOMContentLoaded', function() {
    // Função para verificar se todos os campos de arquivos têm pelo menos um arquivo e se os tipos são válidos
    function verificarArquivos(event) {
        var camposDeArquivos = document.querySelectorAll('input[type="file"]');  // Seleciona todos os inputs do tipo file
        var arquivosValidos = true;
        var allowedTypes = ['application/pdf'];  // Tipos de arquivo permitidos
        var algumCampoVazio = false;  // Variável para verificar se pelo menos um campo está vazio

        // Loop sobre todos os campos de arquivos
        camposDeArquivos.forEach(function(input) {
            if (input.files.length === 0) {  // Verifica se nenhum arquivo foi selecionado
                algumCampoVazio = true;  // Marca como vazio se algum campo não tiver arquivos
            } else {
                // Verifica se os tipos de arquivo são válidos
                for (var i = 0; i < input.files.length; i++) {
                    var file = input.files[i];

                    if (allowedTypes.indexOf(file.type) === -1) {  // Se o tipo de arquivo não for permitido
                        alert("Formato de arquivo não suportado. Insira apenas arquivos PDF.");
                        arquivosValidos = false;  // Marca como inválido se algum arquivo não for do tipo permitido
                        break;  // Interrompe o loop
                    }
                }
            }
        });

        // Se algum campo estiver vazio, exibe o alerta
        if (algumCampoVazio) {
            alert("Por favor, selecione todos os arquivos.");
            arquivosValidos = false;
        }

        // Se algum campo não for válido, evita o envio do formulário
        if (!arquivosValidos) {
            event.preventDefault();  // Impede o envio do formulário
        }
    }

    // Adiciona o evento para o botão de envio
    document.getElementById("btn").addEventListener("click", verificarArquivos);
});


//------------------------------------------------------------------------empenhos
const uploadForm = document.getElementById("upload-form");

function handleFiles(files) {
    for (let file of files) {
        console.log("File:", file.name);
    }
}

uploadForm.addEventListener("dragover", event => {
    event.preventDefault();
    uploadForm.classList.add("highlight");
});

uploadForm.addEventListener("dragleave", () => {
    uploadForm.classList.remove("highlight");
});

uploadForm.addEventListener("drop", event => {
    event.preventDefault();
    uploadForm.classList.remove("highlight");

    let files = event.dataTransfer.files;
    handleFiles(files);

    // Atualiza o campo de input com os arquivos soltos
    let inputElement = document.getElementById("pdf_file");
    inputElement.files = files;
});

uploadForm.addEventListener("change", event => {
    let files = event.target.files;
    handleFiles(files);
});
