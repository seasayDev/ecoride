<template>
    <div class="help-module">
      <header class="help-header">

        <h1>Expérience Guidée avec Écoride</h1>
      </header>
      <main class="help-content">
        <section class="help-section">
          <h2>Trottinettes Électriques dans le Grand Montréal</h2>
          <p>
            Explorez les rues de Montréal avec l’expérience de location de trottinettes électriques d’Écoride. Nos services sont soigneusement conçus pour vous immerger dans le charme historique et la culture vibrante de cette ville emblématique, tout en vous offrant la commodité et le plaisir d’une trottinette électrique. Que vous souhaitiez flâner le long des rives du Saint-Laurent, visiter les quartiers animés ou découvrir les trésors cachés de Montréal, nos trottinettes vous permettront de le faire en toute simplicité. Profitez de la liberté de vous déplacer à votre rythme, en savourant chaque instant de votre balade.
          </p>
        </section>
        <section class="help-section">
          <h2>À quoi s’Attendre</h2>
          <div class="card">
            <h3>Caractéristiques</h3>
            <p>
              La trottinette électrique est équipée d’un <strong>moteur électrique</strong> qui lui permet de se déplacer sans effort. Plus la puissance du moteur est élevée (exprimée en watts), plus la trottinette sera performante en termes de vitesse et d’accélération. La batterie alimente le moteur. Une capacité de <strong>batterie</strong> plus élevée permettra à la trottinette de parcourir une plus longue distance avant de devoir être rechargée. Le <strong>contrôleur électronique</strong> gère la puissance du moteur et permet de réguler la vitesse et l’accélération de la trottinette. Elles sont conçues pour être légères et faciles à transporter. Leur <strong>poids</strong> varie généralement entre 10 et 20 kg, ce qui les rend pratiques pour les déplacements urbains.
            </p>
          </div>
          <div class="card">
            <h3>Lieux Incontournables</h3>
            <p>Pendant la visite, vous pourrez vous arrêter dans certains des endroits les plus populaires de la métropole. Prenez un moment de détente dans des cafés charmants, explorez les boutiques et appréciez l'atmosphère locale. Nos guides vous guideront vers des trésors cachés et des attractions appréciées, vous garantissant ainsi de profiter pleinement de votre visite.</p>
          </div>
        </section>
        <section class="help-section">
          <h2>Pratique et écologique</h2>
          <p>Les trottinettes électriques d'écoride sont conçues pour le confort et la fiabilité, avec une autonomie totale de 65 km. Elles sont la solution écologique parfaite pour explorer la ville, réduisant votre empreinte carbone tout en offrant un mode de transport amusant et efficace. Notre service de location de trottinettes facilite la navigation dans les rues de Montréal, évitant les embouteillages et les tracas de stationnement.</p>
        </section>
        <section class="help-section">
          <h2>Conditions de Participation chez Écoride</h2>
          <div class="card">
            <h3>Âge Minimum et Permis</h3>
            <p>L’âge minimum pour louer la trotinette en tant que conducteur est de 18 ans. Les individus de moins de 18 ans doivent mandater un garant majeur pour respecter nos conditions d'utilisations et garantir une sécurité pour tous.</p>
          </div>
          <div class="card">
            <h3>Réservation</h3>
            <p>Les expériences guidées en trottinettes électriques doivent être réservées au minimum 24 heures avant l’heure de départ souhaitée, ou à court terme sous réserve de disponibilité. Nous recommandons de réserver au moins 3 jours à l’avance pour garantir le créneau horaire souhaité.</p>
          </div>
          <div class="card">
            <h3>Temps de Tour Officiel</h3>
            <p>Les services de location de trottinettes électriques à Montréal offrent plusieurs options en termes de durée. Vous pouvez louer une trottinette pour une heure, deux heures, trois heures, ou même pour une journée complète. Par exemple, chez nous, la location pour une heure coûte 25 $, pour deux heures 45 $, pour trois heures 60 $, et pour une journée entière 80 $ avec des réductions pour les jours additionnels.</p>
          </div>
          <div class="card">
            <h3>Vitesse et Itinéraire</h3>
            <p>Si un ou plusieurs membres de votre groupe ne sont pas capables de maintenir la vitesse limite (typiquement 10 à 20 km/h sur la plupart des routes de Montréal) après les 15 premières minutes du tour, qui sont intentionnellement à un rythme plus lent, tous les arrêts ne seront pas couverts afin de terminer dans le temps imparti.</p>
          </div>
        </section>
        <section class="help-section">
          <h2>Réservez votre expérience</h2>
          <p>Souhaitez-vous découvrir Montréal comme jamais auparavant? Dès maintenant, réservez votre visite guidée en trottinette électrique avec Écoride! Que vous soyez un voyageur en solitaire, en compagnie d'amis ou à la recherche d'une idée de sortie unique, nos visites proposent une expérience adaptée à tous. Maintenant, réservez votre place et préparez-vous à vivre une expérience mémorable au cœur de la métropole.</p>
          
        </section>
      </main>
      <footer class="help-footer">
        <p>Service Client: 1-866-Ecoride (866-487-6844)</p>
        <p>Tous les jours 9:00-21:00 (EST)</p>
        <p>Email officiel: support@ecoride.ca</p>
        <a href="#" class="btn">
           Chat en ligne
        </a>
      </footer>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'Aide',
    setup() {
      
      const router = useRouter();
  
      return {
  
        router
      };
    }
  });
  </script>
  
  <style scoped>
  .help-module {
    font-family: Arial, sans-serif;
    color: #333;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .banner-image {
    width: 100%;
    height: 200px; 
    object-fit: cover;
    margin-bottom: 20px;
  }
  
  .help-header {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .header-image {
    width: 100%;
    height: auto;
    max-height: 300px;
    object-fit: cover;
    margin-bottom: 20px;
  }
  
  .help-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .help-section {
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 5px;
    background: #f9f9f9;
  }
  
  .help-section h2 {
    margin-top: 0;
  }
  
  .card {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 15px;
    background: #fff;
  }
  
  .help-section a,
  .help-footer a {
    color: #007BFF;
    text-decoration: none;
  }
  
  .help-section a:hover,
  .help-footer a:hover {
    text-decoration: underline;
  }
  
  .help-footer {
    text-align: center;
    margin-top: 20px;
  }
  
  .help-footer p {
    margin: 5px 0;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
    background-color: #007BFF;
    border: 2px solid #0056b3;
    border-radius: 5px;
    text-decoration: none;
    color: white;
    margin-top: 10px;
    font-weight: 400;
    -webkit-font-smoothing: antialiased;
    transform: perspective(1px) scale(1.1);
    opacity: 0.9999;
  }
  
  .btn:hover {
    background-color: #0056b3;
    color: white;
    transform: scale(1.0001);
  }
  
  @media (max-width: 768px) {
    .help-content {
      flex-direction: column;
    }
  }
  </style>