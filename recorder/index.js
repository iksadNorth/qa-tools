(function() {
    if (!window.testToolLogs) {
        window.testToolLogs = [];
    }
  
    function saveLog(entry) {
        window.testToolLogs.push(entry);
        localStorage.setItem('testtool_logs', JSON.stringify(window.testToolLogs));
        console.log(entry);
    }
  
    document.addEventListener('click', function(event) {
        saveLog({
            type: 'click',
            selector: getSelector(event.target),
            timestamp: performance.now() / 1000
        });
    }, true);
  
    document.addEventListener('input', function(event) {
        saveLog({
            type: 'input',
            selector: getSelector(event.target),
            value: event.target.value,
            timestamp: performance.now() / 1000
        });
    }, true);
  
    function getSelector(el) {
        // 간단한 셀렉터 생성 로직 (ID 우선)
        if (el.id) return `#${el.id}`;
        if (el.name) return `[name="${el.name}"]`;
        return el.tagName.toLowerCase();
    }
})();
  