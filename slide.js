function hide(element, val) {
    if (val == true){
	element.style.display="none";
    } else {
	element.style.display="block";
    }
}

function main(reloadonend){
    var delay = 100000;
    var allSections = document.getElementsByTagName("section");
    var current = 0;

    if (allSections.length == 0){
	return;
    }
    //hide all but initial
    for (var i = 1; i < allSections.length; i++){
	hide(allSections[i], true);
    }
    window.setInterval(function() {
	hide(allSections[current], true)
	if ((current+1) == allSections.length){
	    if (reloadonend){
		window.location.reload();
	    } else {
		current=0;
	    }
	} else {
	    current++;
	}
	hide(allSections[current], false)
    }, delay);
    
}

main(true);

//<script src="slide.js"></script>
