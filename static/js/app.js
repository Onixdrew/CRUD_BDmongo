base64url=null


async function visualizarFoto(evento){
    const files=evento.target.files
    const archivo=files[0]
    let fileName=archivo.name
    let extencion=fileName.split('.').pop()
    extencion=extencion.tolowerCase()
    
    if(extencion!=='jpg'){

        fileFoto.value=''
        swal.fire('Seleccionar','la imagen debe ser en formato JPG','warning')

    }else{
        base64url=await encodeFileAsBase64URL(archivo)
        const objectURL=URL.createObjectURL(archivo)
        imagenProducto=setAttribute('src',objectURL)
    }


    /**
     * Returns a file in Base64URL format.
     * @param {File} file
     * @return {Promise<string>}
     */
    async function encodeFileAsBase64URL(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.addEventListener('loadend', () => {
                resolve(reader.result);
            });
            reader.readAsDataURL(file);
        });
    };
}

// function agregarProducto(){

//     const foto={
//         foto:base64url
//     }

//     const datos={
//         producto:producto,
//         foto:foto
//     }
//     const url='/agregarProductoJson'
//     fetch(url,{
//         method:'POST',
//         body:JSON.stringify(datos),
//         headers:{
//             'content-Type':
//         }
//     })


// }
