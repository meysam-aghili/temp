function Add(val) {
    var v = document.getElementById('output');
    v.value += val;
 }
 function Solve() {
    var num1 = document.getElementById('output').value;
    document.getElementById('output').value = eval(num1);
 }
 function Clear() {
    var inp = document.getElementById('output');
    inp.value = '';
 }