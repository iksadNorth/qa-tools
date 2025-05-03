(function() {
    var STORE_KEY = 'testtool_logs';
    console.log('inject!');

    if (!window.testToolLogs) {
        window.testToolLogs = [];
    }
  
    function saveLog(entry) {
        window.testToolLogs.push(entry);
        localStorage.setItem(STORE_KEY, JSON.stringify(window.testToolLogs));
        console.log(entry);
    }
  
    window.getLog = function() {
        var logs = window.localStorage.getItem(STORE_KEY);
        window.localStorage.removeItem(STORE_KEY);
        console.log(logs)
        return logs;
    }
  
    function cssPath(el) {
        if (!(el instanceof Element)) return '';
        const path = [];
        while (el.nodeType === Node.ELEMENT_NODE) {
            let selector = el.nodeName.toLowerCase();
            if (el.id) {
                selector += '#' + el.id;
                path.unshift(selector);
                break; // ID는 고유하므로 여기서 멈춤
            } else {
                let sib = el, nth = 1;
                while ((sib = sib.previousElementSibling)) {
                    if (sib.nodeName.toLowerCase() === selector) nth++;
                }
                selector += `:nth-of-type(${nth})`;
            }
            path.unshift(selector);
            el = el.parentNode;
        }
        return path.join(' > ');
    }

    window.run = function() {
        // navigate 로그
        if (!window.prevUrl) {
            saveLog({
                type: 'navigate',
                to: (window.prevUrl = window.location.href),
            });
        }
      
        // click 로그
        window.document.addEventListener('click', function(event) {
            saveLog({
                type: 'click',
                selector: cssPath(event.target),
            });
        }, true);
      
        // input 로그
        window.document.addEventListener('input', function(event) {
            saveLog({
                type: 'input',
                selector: cssPath(event.target),
                value: event.target.value,
            });
        }, true);
    }
})();
  