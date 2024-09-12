<template>
    <div>
      <header>
        <!-- Print username if available -->
        <h1><span v-if="username" class="logged-in-user">{{ username }} Dashboard</span></h1>
        <button @click="showEmailPopup=true" class="action-button edit-button">Update Email</button>
        <router-link :to="{ name: 'statPage' }" v-slot="{ navigate }">
          <button  class="btn-box" @click="navigate">Statistics</button>
        </router-link>
        <router-link :to="{ name: 'myBooks' }" v-slot="{ navigate }">
          <button  class="btn-box" @click="navigate">My Books</button>
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
          <div v-for="(sectionBooks, sectionName) in Sections" :key="sectionName">
            <h2 class="section-title">{{ sectionName }}</h2>
            <div class="section-books">
              <div v-for="(book, index) in sectionBooks" :key="index" class="book-item">
                <div class="book-details">
                  <span>{{ book.name }} by {{ book.author }} - ISBN: {{ book.isbn }} - Pages: {{ book.pages }} - Edition: {{ book.edition }}</span>
                </div>
                <div class="book-actions">
                  <button @click="getBook(book)" class="action-button get-button">Request</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <footer>
      </footer>
    </div>
    <!--delete Book Popup -->
    <div v-if="showRequestPopUp" class="popup">
        <div class="popup-content">
          <!-- Close button at top right -->
          <span @click="showRequestPopUp = false;" class="close">&times;</span>
          <!-- Heading with ISBN of the book -->
          <h2>{{ request_book.isbn }}</h2>
          <!-- Display book details -->
          <div class="form-group">
            <label>Book Name: <span>{{ request_book.name }}</span></label>
          </div>
          <div class="form-group">
            <label>Author: <span>{{ request_book.author }}</span></label>
          </div>
          <div class="form-group">
            <label>Pages: <span>{{ request_book.pages }}</span></label>
          </div>
          <div class="form-group">
            <label>Edition: <span>{{ request_book.edition }}</span></label>
          </div>
          <div class="form-group">
            <label>Publisher: <span>{{ request_book.publisher }}</span></label>
          </div>

           <!-- Input field for Days -->
          <div class="form-group">
            <label for="days">Days:</label>
            <input id="days" name="days" v-model="request_days" placeholder="Enter days">
          </div>

          <!-- Submit button -->
          <div class="form-group">
            <button @click="submitRequestForm" class="submit-button">Submit Request</button>
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

</template>

<script>
import axiosFetch from '../../axios';
export default {
  async mounted() {
    await axiosFetch.get('/user/info').then(response => {
        // Update the username in the component's data with the username received from the backend
        this.username = response.data.username;
        this.editEmail = response.data.email;
        console.log(response.data.username);
      })
      .catch(error => {
        console.error('Error fetching user information:', error);
      });
    axiosFetch.get('/all/book').then(resp =>{
      this.Sections = resp.data;
      console.log('Books fetched:', resp.data);
    })
    .catch(error => {
      console.error('Error in fetching books data:', error);
    });
  },
  data() {
    return {
      username: null,
      editEmail: null,
      showEmailPopup:false,
      Sections: {},
      showRequestPopUp: false,
      request_book: {},
      request_days: '',
      requested_book: {},
      searchPopUp: false,
      searchStatus: '',
      searchQuery:'',
      filter:''
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
      console.log(this.editEmail)
      axiosFetch.put(`/user/email`, {"email":this.editEmail}).then(resp=> {
        console.log(resp.data)
      })
      this.showEmailPopup=false;
    },
    getBook(Book){
      this.request_book = Book;
      this.showRequestPopUp = true;
    },
    submitRequestForm() {
      this.requested_book = {
        'isbn': this.request_book.isbn,
        'username': this.username,
        'days': this.request_days,
        'status_code': 0
      }
      axiosFetch.get('/check').then(resp =>{
        if (resp.data ){
          axiosFetch.post('/request/book', this.requested_book)
            .then(resp=>{
            console.log(resp);
            this.showRequestPopUp = false;
            })
            .catch(error=>{
              console.log(error);
            });
        } 
      }) 
      
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
  }
}
</script>

<style scoped>
  /* Styling for section titles */
  .section-title {
    margin-left: 20px;
    color: #333;
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
  .get-button {
    background-color: #4CAF50;
    color: white;
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
  background-color: #4CAF50;
  color: white;
}

/* Styling for input field */
.input-field {
  padding: 8px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
}

/* Styling for submit button */
.submit-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #45a049;
}
/* Styling for popup */
.popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 20px;
    z-index: 9999; /* Ensure the popup appears above other content */
  }

  /* Styling for popup content */
  .popup-content {
    max-width: 400px; /* Adjust as needed */
    margin: auto;
  }

  /* Styling for close button */
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
    color: red;
  }
</style>