(function() {
    var STORE_KEY = 'testtool_logs';
    var MONITOR_KEY = 'testtool_monitor';
    console.log('recorder inject!');

    function getMonitoring() {
        if(
            window.localStorage.getItem(MONITOR_KEY) === undefined ||
            window.localStorage.getItem(MONITOR_KEY) === null
        ) window.localStorage.setItem(MONITOR_KEY, false);
        boolString = window.localStorage.getItem(MONITOR_KEY);
        return boolString === 'true';
    }
    function setMonitoring(flag) {
        window.localStorage.setItem(MONITOR_KEY, flag);
    }
  
    function getLog() {
        var logs = window.localStorage.getItem(STORE_KEY);
        window.localStorage.removeItem(STORE_KEY);
        return logs;
    }
    function saveLog(entry) {
        if(!getMonitoring()) return;

        var logs = window.localStorage.getItem(STORE_KEY) ?? '[]';
        logs = JSON.parse(logs);
        logs.push(entry);
        localStorage.setItem(STORE_KEY, JSON.stringify(logs));

        console.log(entry);
    }
  
    function cssPath(el) {
        if (!(el instanceof Element)) return '';
        const path = [];
        while (el && el.nodeType === Node.ELEMENT_NODE) {
            let selector = el.nodeName.toLowerCase();

            if (selector === 'body') {
                path.unshift(selector);
                break;
            } else if (el.id && typeof el.id === 'string' && el.id.trim() !== '') {
                selector += `[id="${el.id}"]`;
                path.unshift(selector);
                break;
            }

            let sib = el, nth = 1;
            while ((sib = sib.previousElementSibling)) {
                if (sib.nodeName.toLowerCase() === selector) nth++;
            }
            selector += `:nth-of-type(${nth})`;
            path.unshift(selector);
            el = el.parentNode;
        }
        return path.join(' > ');
    }

    function monitor() {
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
    monitor();

    // 전역 변수 등록
    window.recorder = {};
    window.recorder.getLog = getLog;

    window.recorder.injected = true;
    window.recorder.start = () => {
        setMonitoring(true);
        saveLog({
            type: 'navigate',
            to: (window.prevUrl = window.location.href),
        });
    };
    window.recorder.stop = () => {
        setMonitoring(false);
    };
})();
  