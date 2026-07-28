// for (let i = 1; i <= 5; i++) {
//     let row = "";
//     for (let j = 1; j <= i; j++) {
//         row+=j+" "
//     }
            
//     console.log(row);
// }

let books = ["Гарри Поттер и философский камень", "Гарри Поттер и тайная комната ", "Гарри Поттер и Узник Азкабана"];
books.splice(1, 0, "Гарри Поттер и кубок огня", "Гарри Поттер и Орден Феникса");
console.log(books); 


const prompt = require('prompt-sync')();


let arr=[];
for(i=0;i<5;i++){
    const number = prompt('Введите число: ');
    arr.push(number);
    
}
for(i=0;i<5;i++){
    if(arr[i]%2==0){
        arr.splice(i,1)
    }

}
console.log(arr)

