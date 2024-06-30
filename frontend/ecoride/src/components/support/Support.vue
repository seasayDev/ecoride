<template>
  <div class="container mt-5">
    <h1>Comment voulez vous nous joindre ?</h1>

    
    <div class="mb-3">
      <h2>Contactez-nous par Téléphone</h2>
      <p>Vous pouvez nous contacter à nos heures d'ouvertures du lundi au vendredi de 8h à 18h aux numéros de téléphone suivants :</p>
      <ul>
        <li>+1 123 456 7890</li>
        <li>+1 098 765 4321</li>
      </ul>
    </div>

    
    <div class="mb-3">
      <h2>Contactez-nous par Email</h2>
      <form @submit.prevent="submitEmail">
        <div class="mb-3">
          <label for="email" class="form-label">Votre Email:</label>
          <input type="email" id="email" class="form-control" v-model="email">
        </div>
        <div class="mb-3">
          <label for="message" class="form-label">Message:</label>
          <textarea id="message" class="form-control" v-model="message"></textarea>
        </div>
        <button type="submit" class="btn btn-dark">Envoyer</button>
      </form>
      <p v-if="emailConfirmation" class="alert alert-success mt-3">{{ emailConfirmation }}</p>
    </div>

    <!-- Section Chat en direct -->
    <div class="mb-3">
      <h2>Contactez-nous par Chat en direct</h2>
      <button @click="openChat" class="btn btn-primary">Chat en direct</button>
    </div>

    <!-- Chat Box -->
    <div v-if="showChat" class="chat-box">
      <div class="chat-header">
        <h5>Live-Chat</h5>
        <button @click="closeChat" class="btn-close">×</button>
      </div>
      <div class="chat-body">
        <p>Un de nos agents sera avec vous dans un instant.</p>
        <div class="messages">
          <div v-for="(msg, index) in chatMessages" :key="index" class="message">{{ msg }}</div>
        </div>
        <input type="text" class="form-control" v-model="newMessage" @keyup.enter="sendMessage" placeholder="Tapez votre message ici...">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from 'vue';

export default defineComponent({
  name: 'Support',
  setup() {
    const email: Ref<string> = ref('');
    const message: Ref<string> = ref('');
    const emailConfirmation: Ref<string> = ref('');
    const showChat: Ref<boolean> = ref(false);
    const chatMessages: Ref<string[]> = ref([]);
    const newMessage: Ref<string> = ref('');

    const submitEmail = () => {
      console.log('submitEmail called');  
      emailConfirmation.value = "Nous avons bien reçu votre demande.";
      email.value = '';
      message.value = '';
      console.log('Email Confirmation:', emailConfirmation.value);  
    };

    const openChat = () => {
      console.log('openChat called');
      showChat.value = true;
      console.log('Show Chat:', showChat.value); 
    };

    const closeChat = () => {
      showChat.value = false;
    };

    const sendMessage = () => {
      if (newMessage.value.trim() !== '') {
        chatMessages.value.push(newMessage.value);
        newMessage.value = '';
      }
    };

    return {
      email,
      message,
      emailConfirmation,
      showChat,
      chatMessages,
      newMessage,
      submitEmail,
      openChat,
      closeChat,
      sendMessage
    };
  }
});
</script>

<style scoped>
.container {
  background-color: var(--blue-light);
  padding: 20px;
  border-radius: 8px;
}

.chat-box {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 300px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.chat-header {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-body {
  padding: 10px;
}

.messages {
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.message {
  background-color: #f1f1f1;
  padding: 5px;
  border-radius: 5px;
  margin-bottom: 5px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
</style>
