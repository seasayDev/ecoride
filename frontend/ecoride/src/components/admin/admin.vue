<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mt-5">
      <h1>Gestion des Trotinettes</h1>
    </div>
    <div class="admin-navigation mt-3 mb-3">
      <router-link to="/promotions" class="btn btn-secondary">Voir les Promotions</router-link>
    </div>
    <table class="table mt-3">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Name</th>
          <th scope="col">Location</th>
          <th scope="col">Price $/h</th>
          <th scope="col">Image</th>
          <th scope="col">Categorie</th>
          <th scope="col">Quantite</th>
          <th scope="col">Modifier</th>
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
            <div>
              <button class="btn btn-info" @click="editProduct(index)"><i class="bi bi-pencil-square"></i></button>
              <button class="btn btn-danger ms-2" @click="deleteProduct(index)"><i class="bi bi-trash"></i></button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="d-flex justify-content-center align-items-center">
      <button type="button" class="btn btn-primary" @click="showModalAddProduct">Ajouter produit</button>
    </div>
    <ProductsModal :isVisible="state.showProductModal" @close="closeModal" :locations="state.locations" />
    <EditProduct :isVisible="state.showEditProduct" @close="closeEditModal" :trotinette="state.productToEdit"
      :locations="state.locations" @update="updateProductsTable" />
    <DeleteProduct :isVisible="state.isDeleteModalVisible" @close="hideDeleteModal"
      :trotinette="state.scooterTodelete">
    </DeleteProduct>
  </div>
</template>

<script lang="ts">
import { defineComponent, inject, onMounted, reactive, ref } from 'vue'
import { GetTrotinettes, Trotinette, Location } from './admin'
import ProductsModal from './modals/ProductsModal.vue';
import EditProduct from './modals/EditProduct.vue';
import DeleteProduct from './modals/DeleteProduct.vue';

export default defineComponent({
  components: {
    ProductsModal,
    EditProduct,
    DeleteProduct
  },
  setup() {
    const trotinettes = inject('getTrotinettes') as GetTrotinettes
    const state = reactive({
      trotinettes: [] as Array<Trotinette>,
      showProductModal: false,
      showEditProduct: false,
      isDeleteModalVisible: false,
      productToEdit: {} as Trotinette,
      locations: [] as Array<Location>,
      scooterTodelete: {} as Trotinette
    })

    onMounted(async () => {
      state.trotinettes = await trotinettes.getTrotinettes();
      state.locations = await trotinettes.getLocations()
    })

    const showModalAddProduct = () => {
      state.showProductModal = true
    };
    const closeModal = () => {
      state.showProductModal = false;
      updateProductsTable()
    };
    const closeEditModal = () => {
      state.showEditProduct = false
      updateProductsTable()
    }
    const editProduct = (index: number) => {
      state.showEditProduct = true
      state.productToEdit = state.trotinettes[index]
    }
    const deleteProduct = (index: number) => {
      state.scooterTodelete = state.trotinettes[index]
      state.isDeleteModalVisible = true
    }
    const hideDeleteModal = () => {
      state.isDeleteModalVisible = false;
      updateProductsTable()
    }
    const getImageSrc = (imageData: string) => {
      return `data:image/webp;base64,${imageData}`;
    };

    const updateProductsTable = async () => {
      state.trotinettes = await trotinettes.getTrotinettes();
      state.locations = await trotinettes.getLocations()
    }
    return {
      trotinettes,
      state,
      showModalAddProduct,
      closeModal,
      editProduct,
      closeEditModal,
      getImageSrc,
      deleteProduct,
      updateProductsTable,
      hideDeleteModal
    }
  },
})
</script>

<style scoped>
.scooter-img {
  max-width: 2rem;
}

.admin-navigation {
  display: flex;
  justify-content: flex-end;
}
</style>
