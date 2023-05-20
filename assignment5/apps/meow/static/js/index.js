// This will be the object that will contain the Vue attributes
// and be used to initialize it.

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = function () {

    var self = {};
    
    // This is the Vue data.
    self.data = {
        names: [], 
        text: " ",
        users: "",
        response: "Whats good",
        rowresp: [],
        email: "",
        submit: false,
        isFollowed: false,
        isUnfollowRed: false,
        
       
    };    
    
    self.enumerate = function (a) {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };    

    self.get_curr_user = function(){
        axios.get(cur_user).then(function(response){
            self.vue.users =response.data.cur_user;
            
        })
    }

    self.toggle_follow = function (user) {
        // Perform the necessary follow/unfollow logic her
        // Toggle the isFollowed property of the user
        user.isFollowed = !user.isFollowed;
      };

    self.submitstatus = function(stat){
        self.add_post();
        self.vue.add_post_text = "";
        self.vue.submit = stat;
    }

    self.add_post = function(){
        axios.post(added_post,
            {
                post_text: self.vue.text
            }).then(function (response) { self.vue.rowresp.push({
                postid: response.data.postid,
                post_text: self.vue.add_text,
                name: response.data.name,
                email: response.data.email
            });
            //reset form
            self.vue.text="";
            
            self.enumerate(self.vue.rowresp);
        });
    }
    self.get_users = function () {
        axios.get(get_my_users).then(function (response) {
          self.vue.names = self.enumerate(response.data.users).map(function (user) {
            return {
              username: user.username,
              isFollowed: false,
            };
          });
        });
      };
   

    self.methods = {
        add_post: self.add_post,
        submitstatus: self.submitstatus,
        toggle_follow: self.toggle_follow
     };
    
    // This creates the Vue instance.
    self.vue = new Vue({
        el: "#vue-target",
        data: self.data,
        methods: self.methods
    });

    // Put here any initialization code.
    self.get_users();
    self.get_curr_user();
    // self.toggle_follow();
    return self;
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it. 
var app = init();