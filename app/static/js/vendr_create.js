
function getSelectValue(){
    var selectBox = document.getElementById('vendor')
    var userInput = selectBox.options[selectBox.selectedIndex].value
    var r = document.createRange();
    switch(userInput) {
        case '”PostgreSQL”':
            navigator.clipboard.writeText('username:password@host:port/dbname')
            r.selectNode();

        case '”MySQL”':
            navigator.clipboard.writeText("Server=<server>;Database=<database>;UID=<user id>;PWD=<password>")

            r.selectNode();

        case '”SQLite”':
            navigator.clipboard.writeText('dbname')
            r.selectNode();

    }
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(r);
    window.getSelection().removeAllRanges();
}
const list = document.querySelector('#list');
list.addEventListener('change', function(e) {
  getSelectValue(e)
});
