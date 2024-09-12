<template>
    <div>
      <header>
        <!-- Print username if available -->
        <h1><span v-if="username" class="logged-in-user">{{ username }} Dashboard</span></h1>
        <button @click="showEmailPopup=true" class="action-button edit-button">Update Email</button>
        <router-link :to="{ name: 'statPage' }" v-slot="{ navigate }">
          <button  class="btn-box" @click="navigate">Statistics</button>
        </router-link>
        <router-link :to="{ name: 'requestPage' }" v-slot="{ navigate }">
          <button  class="btn-box" @click="navigate">Book Requests</button>
        </router-link>
        <router-link :to="{name: 'firstPage'}" v-slot="{ navigate }">
          <button class="btn-box" @click="handleLogoutAndNavigate(navigate)">Log Out</button>
        </router-link>

      </header>
      <main>
        <!-- Search bar and search button -->
        <div class="search-container">
          <input type="text" v-model="searchQuery" placeholder="Search...">
          <button @click="search" class="search-button">Search</button>
          <label for="filter">Filter By</label>
          <select name="filter" v-model="filter">
            <option value="name" >Name</option>
            <option value="section" >Section</option>
            <option value="author" >Author</option>
          </select>
        </div>
        <div>
          <div v-for="(sectionBooks, sectionName, index) in Sections" :key="sectionName">
            <h2 class="section-title">{{ sectionName }}</h2>
            <div class="section-books">
              <div v-for="(book, index) in sectionBooks" :key="index" class="book-item">
                <div class="book-details">
                  <span>{{ book.name }} by {{ book.author }} - ISBN: {{ book.isbn }} - Pages: {{ book.pages }} - Edition: {{ book.edition }}</span>
                </div>
                <div class="book-actions">
                  <button @click="editBook(book)" class="action-button edit-button">Edit</button>
                  <button @click="deleteBook(book)" class="action-button delete-button">Delete</button>
                </div>
              </div>
            </div>
            <div class="separator" v-if="index !== Object.keys(Sections).length - 1"></div>
            <div class="section-actions">
              <button @click="addBook(sectionName)" class="action-button add-button">Add Book</button>
              <button @click="editSection(sectionName)" class="action-button edit-button">Edit Section</button>
              <button @click="deleteSection(sectionName)" class="action-button delete-button">Delete Section</button>
            </div>
          </div>
        </div>
      </main>
      <footer>
        <button class="bottom-right-btn" id="add" @click="showPopup = true">+</button>
  
        <!-- Popup -->
        <div v-if="showPopup" class="popup">
          <div class="popup-content">
            <!-- Close button at top right -->
            <span @click="closePopup" class="close">&times;</span>
            <h2>Details to add the book</h2>
            <form @submit.prevent="submitForm">
              <div class="form-group">
                <label for="sections">Section:</label>
                <select id="sections" name="sections" v-model="selectedSection">
                  <option v-for="(section, index) in sections" :key="index" :value="section">{{ section }}</option>
                  <option value="other">Other</option>
                </select>
                <!-- Conditional input field for "other" section -->
                <div v-if="selectedSection === 'other'" class="input-group">
                  <label for="otherSectionInput">Other Section:</label>
                  <input id="otherSectionInput" name="otherSectionInput" v-model="otherSection.section" placeholder="Enter other section">
                </div>
              </div>
              <!-- Common input fields -->
              <div class="form-group">
                <label for="name">Name:</label>
                <input id="name" name="name" v-model="otherSection.name" placeholder="Enter Name">
              </div>
              <div class="form-group">
                <label for="author">Author:</label>
                <input id="author" name="author" v-model="otherSection.author" placeholder="Enter author">
              </div>
              <div class="form-group">
                <label for="isbn">ISBN:</label>
                <input id="isbn" name="isbn" v-model="otherSection.isbn" placeholder="Enter ISBN">
              </div>
              <div class="form-group">
                <label for="publisher">Publisher:</label>
                <input id="publisher" name="publisher" v-model="otherSection.publisher" placeholder="Enter publisher">
              </div>
              <div class="form-group">
                <label for="pages">Pages:</label>
                <input id="pages" name="pages" v-model="otherSection.pages" placeholder="Enter pages">
              </div>
              <div class="form-group">
                <label for="edition">Edition:</label>
                <input id="edition" name="edition" v-model="otherSection.edition" placeholder="Enter edition">
              </div>
              <!-- Submit button -->
              <div class="form-group">
                <button type="submit" class="submit-button">Submit</button>
              </div>
            </form>
          </div>
        </div>
      </footer>
      <!--edit Book Popup -->
      <div v-if="editBookshowPopup" class="popup">
        <div class="popup-content">
          <!-- Close button at top right -->
          <span @click="this.editBookshowPopup = false;" class="close">&times;</span>
          <!-- Heading with ISBN of the book -->
          <h2>{{ editedBook.isbn }}</h2>
          <!-- Form for editing book details -->
          <form @submit.prevent="submitEditForm">
            <!-- Input field for book name -->
            <div class="form-group">
              <label for="editName">Book Name:</label>
              <input id="editName" name="editName" v-model="editedBook.name" placeholder="Enter Book Name">
            </div>
            <!-- Input field for author name -->
            <div class="form-group">
              <label for="editAuthor">Author:</label>
              <input id="editAuthor" name="editAuthor" v-model="editedBook.author" placeholder="Enter Author Name">
            </div>
            <div class="form-group">
              <label for="editPages">Pages:</label>
              <input id="editPages" name="editPages" v-model="editedBook.pages" placeholder="Enter Pages">
            </div>
            <div class="form-group">
              <label for="editEdition">Edition:</label>
              <input id="editEdition" name="editEdition" v-model="editedBook.edition" placeholder="Enter Edition">
            </div>
            <!-- Submit button -->
            <div class="form-group">
              <button type="submit" class="submit-button">Submit</button>
            </div>
          </form>
        </div>
      </div>

      <!--delete Book Popup -->
      <div v-if="deleteBookshowPopup" class="popup">
        <div class="popup-content">
          <!-- Close button at top right -->
          <span @click="deleteBookshowPopup = false;" class="close">&times;</span>
          <!-- Heading with ISBN of the book -->
          <h2>{{ deletedBook.isbn }}</h2>
          <!-- Display book details -->
          <div class="form-group">
            <label>Book Name: <span>{{ deletedBook.name }}</span></label>
          </div>
          <div class="form-group">
            <label>Author: <span>{{ deletedBook.author }}</span></label>
          </div>
          <div class="form-group">
            <label>Pages: <span>{{ deletedBook.pages }}</span></label>
          </div>
          <div class="form-group">
            <label>Edition: <span>{{ deletedBook.edition }}</span></label>
          </div>
          <!-- Submit button -->
          <div class="form-group">
            <button @click="submitDeleteForm" class="delete-button">Delete</button>
          </div>
        </div>
      </div>

    <!-- Popup for adding a book -->
    <div v-if="showAddBookPopup" class="popup">
      <div class="popup-content">
        <!-- Close button at top right -->
        <span @click="closeAddBookPopup" class="close">&times;</span>
        <!-- Show the selected section name -->
        <h2>Section: {{ addSelectedSection }}</h2>
        <!-- Form for adding book details -->
        <form @submit.prevent="submitAddBook">
          <!-- Input field for book name -->
          <div class="form-group">
            <label for="name">Name:</label>
            <input id="name" name="name" v-model="bookDetails.name" placeholder="Enter Name">
          </div>
          <!-- Input field for author name -->
          <div class="form-group">
            <label for="author">Author:</label>
            <input id="author" name="author" v-model="bookDetails.author" placeholder="Enter author">
          </div>
          <!-- Input field for ISBN -->
          <div class="form-group">
            <label for="isbn">ISBN:</label>
            <input id="isbn" name="isbn" v-model="bookDetails.isbn" placeholder="Enter ISBN">
          </div>
          <div class="form-group">
            <label for="publisher">Publisher:</label>
            <input id="publisher" name="publisher" v-model="bookDetails.publisher" placeholder="Enter ISBN">
          </div>
          <!-- Input field for pages -->
          <div class="form-group">
            <label for="pages">Pages:</label>
            <input id="pages" name="pages" v-model="bookDetails.pages" placeholder="Enter pages">
          </div>
          <!-- Input field for edition -->
          <div class="form-group">
            <label for="edition">Edition:</label>
            <input id="edition" name="edition" v-model="bookDetails.edition" placeholder="Enter edition">
          </div>
          <!-- Submit button -->
          <div class="form-group">
            <button type="submit" class="submit-button">Submit</button>
          </div>
        </form>
      </div>
    </div>

    <!--Edit Section name-->
    <div v-if="showEditSectionPopup" class="popup">
      <div class="popup-content">
        <span @click="showEditSectionPopup=false" class="close">&times;</span>
        <h2>Change Section Name</h2>
        <form @submit.prevent="submitEditSectionForm">
          <div class="form-group">
            <label for="editSectionName">New Section Name:</label>
            <input id="editSectionName" name="editSectionName" v-model="editedSectionName" placeholder="Enter New Section Name">
          </div>
          <div class="form-group">
            <button type="submit" class="submit-button">Submit</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Inside your template -->
    <div v-if="showDeleteSectionPopup" class="popup">
      <div class="popup-content">
        <!-- Close button at top right -->
        <span @click="showDeleteSectionPopup=false" class="close">&times;</span>
        <!-- Confirmation message -->
        <h2>Are you sure you want to delete section: {{ deleteSectionName }} and all its books?</h2>
        <!-- Delete button -->
        <div class="form-group">
          <button @click="formDeleteSection" class="delete-button">Delete</button>
        </div>
      </div>
    </div>
    <!--Update email-->
    <div v-if="showEmailPopup" class="popup">
        <div class="popup-content">
          <span @click="showEmailPopup=false" class="close">&times;</span>
          <h2>Update Email</h2>
          <form @submit.prevent="submitEmailForm">
            <div class="form-group">
              <label for="editEmail">Verify Email:</label>
              <input id="editEmail" name="editEmail" v-model="editEmail" placeholder="Enter Email">
            </div>
            <div class="form-group">
              <button type="submit" class="submit-button">Submit</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Search popup -->
      <div v-if="searchPopUp" class="popup">
        <div class="popup-content">
          <!-- Close button at top right -->
          <span @click="searchPopUp=false" class="close">&times;</span>
        
          <h2> {{ searchStatus }}</h2>

          <div class="form-group">
            <button @click="searchPopUp=false" class="submit-button">Ok</button>
          </div>
        </div>
      </div>

    </div>
  </template>
  
  
  

<script>
import axiosFetch from '../../axios';
export default {
  async mounted() {
    await axiosFetch.get('/admin/info').then(response => {
        // Update the username in the component's data with the username received from the backend
        this.username = response.data.username;
        this.editEmail = response.data.email;
        console.log(response.data.username);
      })
      .catch(error => {
        console.error('Error fetching user information:', error);
      });
    axiosFetch.get('/admin/book').then(resp =>{
      this.Sections = resp.data;
      console.log('Books fetched:', resp.data);
    })
    .catch(error => {
      console.error('Error in fetching books data:', error);
    });
    axiosFetch.get('/admin/sections').then(response=> {
      this.sections = response.data.sections;
      console.log('Data fetched:', response.data.sections);
    })
    .catch(error => { 
      console.error('Error fetching data:', error);
    });
  },
  data() {
    return {
      filter:'',
      searchQuery: '',
      userName: null,
      editEmail: null,
      showEmailPopup:false,
      Sections: {},
      sections: [],
      showPopup: false,
      selectedSection: '',
      otherSection: {
        name: '',
        author: '',
        publisher: '',
        pages: '',
        edition: '',
        isbn: '',
        section: '',
      },
      editBookshowPopup: false,
      editedBook: {},
      deleteBookshowPopup: false,
      deletedBook: {},
      showAddBookPopup: false,
      addselectedSection: '', // Will be set when Add Book button is clicked
      bookDetails: {
        name: '',
        author: '',
        isbn: '',
        publisher: '',
        pages: '',
        edition: '',
        section: '',
      },
      showEditSectionPopup: false,
      editedSectionName: '',
      oldSectionName: '',
      showDeleteSectionPopup: false,
      deleteSectionName: '',
      searchPopUp: false,
      searchStatus: ''
    };
  },
  methods: {
    search(){
      axiosFetch.get(`/search/book?query=${this.searchQuery}&filter=${this.filter}`).then(resp => {
        console.log("searched" , resp.data)
        
        this.searchStatus = resp.data && resp.data.length > 0 ? 'Available' : 'Not Available';
        this.searchPopUp=true

      })
    },
    submitEmailForm() {
      axiosFetch.put(`/admin/email`,{"email": this.editEmail}).then(resp =>{
        console.log(resp.data);
      })
      this.showEmailPopup=false;
    },
    deleteSection(sectionName) {
      this.deleteSectionName=sectionName,
      this.showDeleteSectionPopup= true
    },
    formDeleteSection() {
      // beckend of delete section 
      axiosFetch.delete(`/admin/section/${this.deleteSectionName}`).then(resp=>{
        console.log(resp.data)
      })
      this.showDeleteSectionPopup= false
    },
    editSection(sectionName) {
      this.oldSectionName = sectionName;
      this.editedSectionName = sectionName;
      this.showEditSectionPopup = true;
    },
    submitEditSectionForm() {
      //Add here
      axiosFetch.put(`/admin/section/${this.oldSectionName}`, {"newName" :this.editedSectionName}).then(resp => {
        console.log(resp.data)
      })
      this.showEditSectionPopup=false;
    },
    addBook(sectionName) {
      this.addSelectedSection = sectionName;
      this.showAddBookPopup = true;
    },
    closeAddBookPopup() {
      this.showAddBookPopup = false;
      // Reset book details
      this.bookDetails = {
        name: '',
        author: '',
        isbn: '',
        pages: '',
        edition: '',
        section: ''
      };
    },
    submitAddBook() {
      // Handle form submission, e.g., sending book details to backend
      this.bookDetails.section = this.addSelectedSection;
      console.log('Book details submitted:', this.bookDetails);
      axiosFetch.post('/admin/book', this.bookDetails)
      .then(resp => {
        console.log(resp);
        this.closeAddBookPopup();// Close popup after successful submission
        })
      .catch(error => {
        if (error.response && error.response.status === 409) {
          console.log("ISBN number should be unique.");
        } else {
          console.error("An error occurred:", error.message);
        }
      });
      
    },
    deleteBook(book){
      this.deletedBook = { ...book };
      this.deleteBookshowPopup = true;
    },

    editBook(book) {
      this.editedBook = { ...book }; // Copy book details to editedBook
      this.editBookshowPopup = true; // Show the popup
    },
    submitEditForm() {
      axiosFetch.put(`/admin/book/${this.editedBook.isbn}`, this.editedBook).then(response=> {
        console.log(response.data);
      });
      this.editBookshowPopup = false;
      
    },
    submitDeleteForm() {
      axiosFetch.delete(`/admin/book/${this.deletedBook.isbn}`).then(resp=> {
        console.log(resp.data)
      })
      // Logic to update book details (e.g., send request to backend)
      // After successful submission, close the popup
      this.deleteBookshowPopup = false;
    },
    
    handleLogoutAndNavigate(navigate) {
        // Call both logout and navigate functions
        this.logout();
        navigate();
      },
    logout() {
 
          localStorage.removeItem('authToken')
          this.$router.push('/login');
    },
    closePopup() {
      this.showPopup = false; // Method to close pop up
      this.resetForm();     //reset the data
    },
    resetForm() {
      this.selectedSection = '';
      this.otherSection = {
        name: '',
        author: '',
        publisher: '',
        pages: '',
        edition: '',
        isbn: '',
        section: '',
      };
    },
    submitForm() {
      if (this.selectedSection == 'other') {
        axiosFetch.post('/admin/book', this.otherSection)
          .then(resp => {
            console.log(resp);
            this.closePopup(); // Close popup after successful submission
          })
          .catch(error => {
            if (error.response && error.response.status === 409) {
              console.log("ISBN number should be unique.");
            } else {
              console.error("An error occurred:", error.message);
            }
          });
      } else {
        this.otherSection.section = this.selectedSection;
        axiosFetch.post('/admin/book', this.otherSection)
          .then(resp => {
            console.log(resp);
            this.closePopup(); // Close popup after successful submission
          })
          .catch(error => {
            if (error.response && error.response.status === 409) {
              console.log("ISBN number should be unique.");
            } else {
              console.error("An error occurred:", error.message);
            }
          });
      }
    }

  }
}
</script>
<style scoped>
  /* Styling for section titles */
  .section-title {
    margin-left: 20px;
    color: #422424;
    font-size: 24px;
  }

  /* Styling for section books */
  .section-books {
    display: flex;
    flex-direction: column;
  }

  /* Styling for book item */
  .book-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    border-bottom: 1px solid #ccc;
  }

  /* Styling for book info */
  .book-info {
    width: 70%;
  }

  /* Styling for book actions */
  .book-actions {
    display: flex;
    align-items: center;
  }

  /* Styling for action buttons */
  .action-button {
    margin-right: 10px;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  }

  /* Styling for edit button */
  .edit-button {
    background-color: #4CAF50;
    color: white;
  }

  /* Styling for delete button */
  .delete-button {
    background-color: #FF5733;
    color: white;
  }

  /* Styling for add button */
  .add-button {
    background-color: #2196F3;
    color: white;
  }

  /* Styling for separator */
  .separator {
    border-bottom: 1px solid #ccc;
    margin: 20px 0;
  }

  /* Styling for section actions */
  .section-actions {
    display: flex;
    align-items: center;
    margin-left: 20px;
  }

  /* Styling for submit button */
  .submit-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
  }

  /* Styling for popup */
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }

  /* Styling for popup content */
  .popup-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);
    width: 400px;
    position: relative;
  }

  /* Styling for close button */
  .close {
    color: red;
    cursor: pointer;
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
  }

  /* Styling for form groups */
  .form-group {
    margin-bottom: 15px;
  }

  /* Styling for form labels */
  label {
    display: block;
    font-weight: bold;
  }

  /* Styling for select and input elements */
  select,
  input {
    width: calc(100% - 20px);
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  /* Styling for footer */
  footer {
    position: fixed;
    bottom: 20px;
    right: 20px;
  }

  /* Styling for add button */
  .bottom-right-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 24px;
    cursor: pointer;
  }
    /* Styling for header */
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #f0f0f0;
    border-bottom: 2px solid #ddd;
    margin-top: 0;
  }

  /* Styling for username */
  .logged-in-user {
    font-size: 20px;
    color: #333;
  }

  /* Styling for buttons */
  .btn-container {
    display: flex;
    align-items: center;
  }

  /* Styling for button */
  .btn {
    margin-left: 10px;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    color: white;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
  }

  /* Styling for header */
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #5e5d5d;
    border-bottom: 2px solid #585656;
    margin-top: 0;
  }

  /* Styling for username */
  .logged-in-user {
    font-size: 20px;
    color: #333;
  }

  /* Styling for buttons */
  .btn-container {
    display: flex;
    align-items: center;
    background-color: #585656;
  }

  /* Styling for button */
  .btn {
    margin-left: 10px;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    color: white;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
  }

/* Styling for search container */
.search-container {
  margin: 20px auto;
  text-align: center;
}

/* Styling for search input */
.search-container input[type="text"] {
  padding: 8px;
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Styling for search button */
.search-button {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #ade53c;
  color: white;
}
</style>


