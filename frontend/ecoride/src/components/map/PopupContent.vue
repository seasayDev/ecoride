<template>
    <div class="popup-content">
      <img src="https://via.placeholder.com/150" alt="Placeholder Image" />
      <button @click="handleButtonClick">Click Me</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopupContent',
    methods: {
      handleButtonClick() {
        alert('Button clicked!');
      }
    }
  };
  </script>
  
  <style scoped>
  .popup-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .popup-content img {
    width: 150px;
    height: 150px;
    margin-bottom: 10px;
  }
  
  .popup-content button {
    padding: 5px 10px;
  }
  </style>
  