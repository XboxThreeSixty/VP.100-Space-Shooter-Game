let rgbList = [250, 0, 0];

function rainbowLoop(rgbList) {
    if(rgbList[0] == 250 && rgbList[1] < 250 && rgbList[2] == 0) {
        rgbList[1] += 1;
    } else if(rgbList[0] > 0 && rgbList[1] == 250 && rgbList[2] == 0) {
        rgbList[0] -= 1;
    } else if(rgbList[0] == 0 && rgbList[1] == 250 && rgbList[2] < 250) {
        rgbList[2] += 1;
    } else if(rgbList[0] == 0 && rgbList[1] > 0 && rgbList[2] == 250) {
        rgbList[1] -= 1;
    } else if(rgbList[0] < 250 && rgbList[1] == 0 && rgbList[2] == 250) {
        rgbList[0] += 1;
    } else if(rgbList[0] == 250 && rgbList[1] == 0 && rgbList[2] > 0) {
        rgbList[2] -= 1;
    }
    return rgbList;
}

function changeColor(rgbList) {
    rgbList = rainbowLoop(rgbList);
    document.getElementById("pageHeader").style.color = `rgb(${rgbList[0]}, ${rgbList[1]}, ${rgbList[2]})`;
    return rgbList;
}

setInterval(changeColor, 1, rgbList);