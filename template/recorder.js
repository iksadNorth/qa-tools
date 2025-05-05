(function() {
    var STORE_KEY = 'testtool_logs';
    console.log('recorder inject!');

    function getMonitoring() {
        if(window.MONITOR_FLAG === undefined) window.MONITOR_FLAG = false;
        return window.MONITOR_FLAG;
    }
    function setMonitoring(flag) {
        window.MONITOR_FLAG = flag;
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
    };
    window.recorder.stop = () => {
        setMonitoring(false);
    };
})();
  