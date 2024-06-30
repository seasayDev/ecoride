<template>
    <div class="product-modal" v-if="isVisible">
        <div class="container">
            <form>
                <button class="close-button" @click="closeModal"><i class="bi bi-x-circle"></i></button>
                <div class="row mb-3 mt-5">
                    <div class="col-md-4">
                        <label for="firstName" class="form-label">Nom</label>
                        <input type="text" class="form-control" id="firstName" placeholder="Entrez le nom" required>
                    </div>
                    <div class="col-md-4">
                        <label for="lastName" class="form-label">Location place</label>
                        <input type="text" class="form-control" id="lastName" placeholder="Entrez la place de location"
                            required>
                    </div>
                    <div class="col-md-4">
                        <label for="country" class="form-label">Prix</label>
                        <input type="text" class="form-control" id="country" placeholder="Entrez le prix" required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="firstName" class="form-label">Image</label>
                        <input type="file" class="form-control" id="firstName" required>
                    </div>
                    <div class="col-md-4">
                        <label for="lastName" class="form-label">Quantite</label>
                        <input type="text" class="form-control" id="lastName" placeholder="Entrez la quntite" required>
                    </div>
                    <div class="col-md-4">
                        <label for="lastName" class="form-label">Categorie</label>
                        <input type="text" class="form-control" id="lastName" placeholder="Entrez la Categorie" required>
                    </div>

                </div>
                <button type="button" class="btn btn-primary mt-5">Submit</button>
            </form>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
    props: {
        isVisible: {
            type: Boolean as PropType<boolean>,
            required: true,
        },
    },
    emits: ['close'],
    setup(props, { emit }) {

        const closeModal = () => {
            emit('close');
        };

        return {
            closeModal,
        };

    },
})
</script>
<style scoped>
.product-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
}

.container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    position: relative;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;

}

.bi {
    color: red;
}

.bi:hover {
    color: blue;
}
</style>
