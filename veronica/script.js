
// const btnEquals = document.getElementById('btnEquals');
// const resultDiv = document.getElementById('result');

// // const num1 = parseFloat(document.getElementById('num1').value);
// // const num2 = parseFloat(document.getElementById('num2').value);


// // btnEquals.addEventListener('click', () => {
// //   let result = 0;
// //   result = num1 + num2;
// //   resultDiv.textContent = result;
// // });
// btnEquals.addEventListener('click', function() {

//   const num1 = parseFloat(document.getElementById('num1').value);
//   const num2 = parseFloat(document.getElementById('num2').value);

//   const sum = num1 + num2;
  
//   resultDiv.textContent = sum;

// });


// class Car{
//   constructor(brand,model,year,mileage){
//     this.brand=brand;
//     this.model=model;
//     this.year=year;
//     this.mileage=mileage;
//   }

//   drive(distance){
//     this.mileage= this.mileage+distance
//   }
//   polomka(){
//     if (this.mileage>50000){
//       console.log("Замените мотор")
//     }
//   }
// }
// const BMW= new Car("BMW","530i",2016,53000);
// BMW.drive(7000)


document.addEventListener('DOMContentLoaded', () => {
  const num1Input = document.getElementById('num1');
  const num2Input = document.getElementById('num2');
  const operatorSelect = document.getElementById('operator');
  const btnEquals = document.getElementById('btnEquals');
  const resultDiv = document.getElementById('result');

  btnEquals.addEventListener('click', () => {

    const num1 = parseFloat(num1Input.value);
    const num2 = parseFloat(num2Input.value);
    const operator = operatorSelect.value; // "+" or "-"

    if (isNaN(num1) || isNaN(num2)) {
      resultDiv.textContent = 'Пожалуйста, введите оба числа';
      resultDiv.style.color = 'red';
      return;
    }

    let result;

    switch (operator) {
      case 'add':
        result = num1 + num2;
        break;
      case 'subtract':
        result = num1 - num2;
        break;
      case 'multiply':
        result = num1 * num2;
        break;
      case 'divide':
        if (num2 === 0) {
          resultDiv.textContent = 'На ноль делить нельзя!';
          resultDiv.style.color = 'red';
          return;
        }
        result = num1 / num2;
        break;
      default:
        result = 'Ошибка';
    }

    const formattedResult = parseFloat(result.toFixed(8));

    resultDiv.textContent = `${formattedResult}`;
    resultDiv.style.color = '#333';
  });
});