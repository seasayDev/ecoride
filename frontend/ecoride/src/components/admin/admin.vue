<template>
    <div class="container">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Location</th>
                    <th scope="col">Price $/h</th>
                    <th scope="col">Image</th>
                    <th scope="col">Quentite</th>
                    <th scope="col">Modifier</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in state.trotinettes" :key="index">
                    <th scope="row">{{ item.id_trotinette }}</th>
                    <td>{{ item.name }}</td>
                    <td>{{ item.location.name }}</td>
                    <td>{{ item.price }}</td>
                    <td><img src="../../images/scooter1.webp" class="scooter-img" /></td>
                    <td>{{ item.qte }}</td>
                    <td><button class="btn btn-info" @click="editProduct(index)"><i
                                class="bi bi-pencil-square"></i></button></td>

                </tr>

            </tbody>
        </table>
        <div>
            <button type="button" class="btn btn-primary" @click="showModalAddProduct">Ajouter
                produit</button>
        </div>

    </div>
    <ProductsModal :isVisible="state.showProductModal" @close="closeModal" />
    <EditProduct :isVisible="state.showEditProduct" @close="closeEditModal" :trotinette="state.productToEdit" />
</template>
<script lang="ts">
import { defineComponent, inject, onMounted, reactive, ref } from 'vue'
import { GetTrotinettes, Trotinette } from './admin'
import ProductsModal from './modals/ProductsModal.vue';
import EditProduct from './modals/EditProduct.vue';

export default defineComponent({
    components: {
        ProductsModal,
        EditProduct
    },
    setup() {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const state = reactive({
            trotinettes: [] as Array<Trotinette>,
            showProductModal: false,
            showEditProduct: false,
            productToEdit: {} as Trotinette
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
        const closeEditModal = () => {
            state.showEditProduct = false
        }
        const editProduct = (index: number) => {
            state.showEditProduct = true
            state.productToEdit = state.trotinettes[index]
            console.log('EDIT', state.productToEdit)
        }
        return {
            trotinettes,
            state,
            showModalAddProduct,
            closeModal,
            editProduct,
            closeEditModal
        }
    },
})
</script>
<style scoped>
.scooter-img {
    max-width: 2rem;
}
</style>
