<template>
    <div>
        <h1>Books</h1>
        <h2>Requested Books</h2>
        <div v-for="instance in req_books" :key="instance.id" class="instance-entry">
            <strong>{{instance.book.name}}</strong> written by 
            <strong> {{ instance.book.author}}</strong>-----Request By:<strong>{{instance.username}}</strong>------for {{  instance.days }} <strong>Days</strong> 
            <button @click="approveRequest(instance.id)">Approve</button>
            <button @click="declineRequest(instance.id)">Decline</button>
            <hr>
        </div>
        <h2>Approved Books</h2>
        <div v-for="instance in get_books" :key="instance.id" class="instance-entry">
            <strong>{{instance.book.name}}</strong> written by 
            <strong> {{ instance.book.author}}</strong>-----Request By:<strong>{{instance.username}}</strong>------for {{  instance.days }} <strong>Days</strong> 
            <button @click="revoke(instance.id)">Revoke</button>
            <hr>  
        </div>
        <h2>Denied Books</h2>
        <div v-for="instance in den_books" :key="instance.id" class="instance-entry">
            <strong>{{instance.book.name}}</strong> written by 
            <strong> {{ instance.book.author}}</strong>-----Request By:<strong>{{instance.username}}</strong>------for {{  instance.days }} <strong>Days</strong> 
            <hr>
        </div>
        <h2>Expired Books</h2>
        <div v-for="instance in exp_books" :key="instance.id" class="instance-entry">
            <strong>{{instance.book.name}}</strong> written by 
            <strong> {{ instance.book.author}}</strong>-----Request By:<strong>{{instance.username}}</strong>------for {{  instance.days }} <strong>Days</strong> 
            <hr>
        </div>
    </div>
    </template>
    
    
    <script>
    import axiosFetch from '../../axios';
    export default {
        data(){
            return { 
                username: null,
                req_books : '',
                status_code_r : 0,
                get_books : '',
                status_code_g:1,
                den_books: '',
                status_code_d:2,
                exp_books : '',
                status_code_e:3,
            }
        }, 
        async mounted() { 
            await axiosFetch.get('/admin/info').then(response => {
                // Update the username in the component's data with the username received from the backend
                this.username = response.data.username;
                console.log(response.data.username);
            })
            .catch(error => {
                console.error('Error fetching user information:', error);
            }); 
            axiosFetch.get(`/book/issued?username=${this.username}&status_code=${this.status_code_r}`)
            .then(resp => {
                //this.req_books = resp.data;
                console.log(resp.data)
                this.req_books= resp.data
            })
            axiosFetch.get(`/book/issued?username=${this.username}&status_code=${this.status_code_g}`)
            .then(resp => {
                //this.req_books = resp.data;
                console.log(resp.data)
                this.get_books= resp.data
            })
            axiosFetch.get(`/book/issued?username=${this.username}&status_code=${this.status_code_d}`)
            .then(resp => {
                //this.req_books = resp.data;
                console.log(resp.data)
                this.den_books= resp.data
            })
            axiosFetch.get(`/book/issued?username=${this.username}&status_code=${this.status_code_e}`)
            .then(resp => {
                //this.req_books = resp.data;
                console.log(resp.data)
                this.exp_books= resp.data
            })
            // ,
            // axiosFetch.delete(`/user/book/1/delete`).then(resp =>{
            //             console.log(resp.data)
            //         })
            },
            methods :{
                approveRequest(id){
                    axiosFetch.put(`/book/${id}/return`,{"status_code":1}).then(resp => {
                        console.log(resp.data);
                    })
                },
                declineRequest(id){ 
                    axiosFetch.put(`/book/${id}/return`,{"status_code":2}).then(resp => {
                        console.log(resp.data);
                    })
                } ,
                revoke(id){
                    axiosFetch.put(`/book/${id}/return`,{"status_code":3}).then(resp => {
                        console.log(resp.data);
                    })
                }
            }
        
    }
    </script>
    
    <style scoped >
    
    </style>