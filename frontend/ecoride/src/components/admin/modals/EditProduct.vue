<template>
    <div class="product-modal" v-if="isVisible">
        <div class="container">
            <form @submit.prevent="editProduct">
                <button class="close-button" @click="closeEditModal"><i class="bi bi-x-circle"></i></button>
                <div class="row mb-3 mt-5">
                    <div class="col-md-4">
                        <label for="firstName" class="form-label">Nom</label>
                        <input type="text" class="form-control" id="firstName" v-model="state.trotinette.name"
                            placeholder="Entrez le nom" required>
                    </div>
                    <div class="col-md-4">
                        <label for="location" class="form-label">Location place</label>
                        <select class="form-select" id="location" v-model="state.trotinette.location.name" required>
                            <option v-for="location in locations" :key="location.id" :value="location.name">
                                {{ location.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-md-4">
                        <label for="country" class="form-label">Prix</label>
                        <input type="text" class="form-control" id="country" v-model="state.trotinette.price"
                            placeholder="Entrez le prix" required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="firstName" class="form-label">Image</label>
                        <input type="file" class="form-control" id="firstName" @change="onFileChange">
                    </div>
                    <div class="col-md-4">
                        <label for="lastName" class="form-label">Quantite</label>
                        <input type="text" class="form-control" v-model="state.trotinette.qte" id="lastName"
                            placeholder="Entrez la quntite" required>
                    </div>
                    <div class="col-md-4">
                        <label for="lastName" class="form-label">Categorie</label>
                        <input type="text" class="form-control" v-model="state.trotinette.category" id="lastName"
                            placeholder="Entrez la categorie" required>
                    </div>

                </div>
                <button type="submit" class="btn btn-primary mt-5">Submit</button>
            </form>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, onMounted, PropType, reactive, watch, inject } from 'vue'
import { Trotinette, Location, Newscooter, GetTrotinettes } from '../admin'
export default defineComponent({
    props: {
        isVisible: {
            type: Boolean as PropType<boolean>,
            required: true,
        },
        trotinette: {
            type: {} as PropType<Trotinette>,
            required: true
        },
        locations: {
            type: {} as PropType<Array<Location>>,
            required: true
        }
    },
    emits: ['close', 'update'],
    setup(props, { emit }) {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const state = reactive({
            trotinette: { ...props.trotinette },
            locations: { ...props.locations },
        })

        watch(() => props.trotinette, (newValue) => {
            state.trotinette = { ...newValue }

        }, { immediate: true })
        watch(() => props.locations, (newValue) => {
            state.locations = { ...newValue }
        }, { immediate: true })

        const closeEditModal = () => {
            emit('close');
        };
        const onFileChange = (event: Event) => {
            const input = event.target as HTMLInputElement;
            if (input.files && input.files[0]) {
                const file = input.files[0];
                const validTypes = ['image/webp', 'image/png'];
                if (!validTypes.includes(file.type)) {
                    alert('Please select a .webp or .png file.');
                    input.value = '';
                    return;
                }
                const reader = new FileReader();
                reader.onload = () => {
                    state.trotinette.image = {
                        id: state.trotinette.image?.id || null,
                        data: reader.result.split(',')[1] as string
                    };
                };
                reader.readAsDataURL(file);
            }
        };

        const editProduct = async () => {
            const result = {
                id_trotinette: state.trotinette.id_trotinette,
                name: state.trotinette.name,
                category: state.trotinette.category,
                price: state.trotinette.price,
                available: state.trotinette.available,
                location: { ...state.trotinette.location },
                image: { ...state.trotinette.image },
                qte: state.trotinette.qte,
            }
            await trotinettes.updateScooter(result)
            emit('update', state.trotinette);
            closeEditModal();

        }
        return {
            closeEditModal,
            state,
            editProduct,
            onFileChange,
            trotinettes
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
