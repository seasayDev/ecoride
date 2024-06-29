<template>
    <div class="container">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Location id</th>
                    <th scope="col">Price $/h</th>
                    <th scope="col">Image id</th>
                    <th scope="col">Quentite</th>


                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in state.trotinettes" :key="index">
                    <th scope="row">{{ item.id_trotinette }}</th>
                    <td>{{ item.name }}</td>
                    <td>{{ item.location_id }}</td>
                    <td>{{ item.price }}</td>
                    <td>{{ item.image_id }}</td>
                    <td>{{ item.qte }}</td>
                </tr>

            </tbody>
        </table>
        <div>
            <button type="button" class="btn btn-primary" @click="showModalAddProduct">Ajouter
                produit</button>
        </div>

    </div>
    <productsModal :isVisible="state.showProductModal" @close="closeModal" />
</template>
<script lang="ts">
import { defineComponent, inject, onMounted, reactive, ref } from 'vue'
import { GetTrotinettes, trotinette } from './admin'


import ProductsModal from './modals/ProductsModal.vue';

export default defineComponent({
    components: {
        ProductsModal
    },
    setup() {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const state = reactive({
            trotinettes: [] as Array<trotinette>,
            showProductModal: false

        })

        onMounted(async () => {
            state.trotinettes = await trotinettes.getTrotinettes();
            console.log(state.trotinettes)
        })
        const showModalAddProduct = () => {
            state.showProductModal = true
        };
        const closeModal = () => {
            state.showProductModal = false;
        };
        return {
            trotinettes,
            state,
            showModalAddProduct,
            closeModal
        }

    },
})
</script>
<style scoped></style>
