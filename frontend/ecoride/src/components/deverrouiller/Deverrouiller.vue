<template>
    <div class="container">
        <table class="table mt-5">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Location</th>
                    <th scope="col">Price $/h</th>
                    <th scope="col">Image</th>
                    <th scope="col">Categorie</th>
                    <th scope="col">Quantite</th>
                    <th scope="col">Déverrouiller</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in state.trotinettes" :key="index">
                    <th scope="row">{{ item.id_trotinette }}</th>
                    <td>{{ item.name }}</td>
                    <td>{{ item.location.name }}</td>
                    <td>{{ item.price }}</td>
                    <td><img :src="getImageSrc(item.image.data)" class="scooter-img" /></td>
                    <td>{{ item.category }}</td>
                    <td>{{ item.qte }}</td>
                    <td>
                        <button class="btn btn-primary" @click="deverrouillerTrotinette(index)">Déverrouiller</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <DeverrouillerModal :isVisible="state.showModal" @close="closeModal" :trotinette="state.selectedTrotinette" @codeSent="handleCodeSent" />
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, onMounted, reactive } from 'vue'
import { GetTrotinettes, Trotinette } from '../admin/admin'
import DeverrouillerModal from './DeverrouillerModal.vue'

export default defineComponent({
    components: {
        DeverrouillerModal
    },
    setup() {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const state = reactive({
            trotinettes: [] as Array<Trotinette>,
            showModal: false,
            selectedTrotinette: {} as Trotinette
        })

        onMounted(async () => {
            state.trotinettes = await trotinettes.getTrotinettes()
        })

        const deverrouillerTrotinette = (index: number) => {
            state.selectedTrotinette = state.trotinettes[index]
            state.showModal = true
        }

        const closeModal = () => {
            state.showModal = false
        }

        const handleCodeSent = async () => {
            alert('Trottinette déverrouillée avec succès!')
            state.trotinettes = await trotinettes.getTrotinettes()
        }

        const getImageSrc = (imageData: string) => {
            return `data:image/webp;base64,${imageData}`
        }

        return {
            state,
            deverrouillerTrotinette,
            closeModal,
            handleCodeSent,
            getImageSrc
        }
    }
})
</script>

<style scoped>
.scooter-img {
    max-width: 2rem;
}
</style>
