function createXHR() {
    if (window.XMLHttpRequest){
        return new XMLHttpRequest()
    }
    else
        return new ActiveXObject()
}