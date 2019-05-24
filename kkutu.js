// ==UserScript==
// @name         kkutu
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://kkutu.co.kr/?server=*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    var ws = new WebSocket('ws://127.0.0.1:15678')
    var observerGameBox = new MutationObserver(function(MutationRecord) {
        if(MutationRecord[0].target.style.display != "none")
        {
            var type = "game"
            var data = document.getElementsByClassName("room-head-mode")[0].textContent
            var sendData = {type, data}
            ws.send(JSON.stringify(sendData))
        }
    })
    var observerQuiz = new MutationObserver(function(MutationRecord) {
        if(MutationRecord[0].target.textContent.indexOf("(") != -1)
        {
            var type = "allowword"
            var data = MutationRecord[0].target.textContent[MutationRecord[0].target.textContent.indexOf("(")+1]
            var sendData = {type, data}
            ws.send(JSON.stringify(sendData))
        }
    })
    var observerHistory = new MutationObserver(function(MutationRecord) {
        var type = "history"
        var data = MutationRecord[0].target.firstChild.firstChild.textContent
        var sendData = {type, data}
        ws.send(JSON.stringify(sendData))
    })
    var observerRounds = new MutationObserver(function(MutationRecord) {
        if(MutationRecord[0].target.textContent == 0)
        {
            var type = "round"
            var data = document.getElementsByClassName('rounds-current')[0].textContent
            var sendData = {type, data}
            ws.send(JSON.stringify(sendData))
        }
    })
    observerGameBox.observe(document.getElementsByClassName('GameBox')[0],{
        attribute:true,
        attributeFilter:["style"]
    })
    observerQuiz.observe(document.getElementsByClassName('jjo-display')[0],{
        childList:true,
        characterData:true
    })
    observerHistory.observe(document.getElementsByClassName('history')[0],{
        childList:true
    })
    observerRounds.observe(document.getElementsByClassName('chain')[0],{
        childList:true,
        characterData:true
    })
})();