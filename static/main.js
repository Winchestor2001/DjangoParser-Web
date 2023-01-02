function optionChange(){
    let form_lang = document.querySelector('.form_lang');
    form_lang.submit();
}
let unchecked = document.querySelectorAll('.unchecked')
unchecked.forEach(elem =>{
    elem.addEventListener('click',()=>{
        elem.checked=false
    })
})

window.onload = () => {
    let loader = document.querySelector('#prelaoder');
    loader.style.opacity = 0;
    loader.style.visibility = "hidden";
}


