document.addEventListener('DOMContentLoaded', function(){
  document.querySelector('#profile').style.display = 'none';    
  window.history.pushState('The Network', 'The Network', 'http://127.0.0.1:8000/');
  if(document.getElementById('following')) {
      document.getElementById('following').addEventListener('click', () => load_posts("/followed",1));          
  }    
  load_posts("",1);
})

function load_posts(addon,page){
  if (addon.includes("?")){
    addon += `&page=${page}`;
  } else {
    document.querySelector('#profile').style.display = 'none';
    addon += `?page=${page}`
  }
  // console.log(addon, page)
  fetch(`/load_posts${addon}`)
  .then(response => response.json())
  .then(response => {
    document.getElementById('posts').innerHTML = "";
    struct_paginator(addon,page,response.num_pages);
    response.posts.forEach(post => struct_post(post));
  })
}
// struct_post/build
function struct_post(post){
  // console.log('girdik')
  const post_card = document.createElement('div');
  post_card.className = "card";

  // const test = document.createElement('p');
  // test.innerHTML = "test";
  // post_card.append(test);
  
  const header = document.createElement('div');
  
  header.className = "card-header text-left userdetail";
  header.style.cursor = "pointer"
  header.innerHTML = `Created by: ${post.post_creator_username}`;
  
  // console.log(post.post_creator_username)
  post_card.append(header);
  
  header.addEventListener('click', () => profile_page(post.post_creator_id));

  const card_body = document.createElement('div');
  card_body.className = "card-body";
  card_body.id = `post_body_${post.post_id}`;
  
  const headerid = document.createElement('div');
  headerid.className = "card border-0 col-0 text-right"
  headerid.innerHTML = `Post# ${post.post_id}`
  
  

  const text = document.createElement('p');
  text.className = "card text-justify border-light";
  text.id = `content_${post.post_id}`;
  text.innerHTML = post.post_content;
  // console.log(post.post_content)
  card_body.append(headerid);
  card_body.append(text);

  const likes_row = document.createElement('div');
  likes_row.className = "row align-items-center";
  likes_row.id = `likes_row_${post.post_id}`;


  // likes icon
  const like_icon = document.createElement('i');
  like_icon.id = `like_icon_${post.post_id}`;
  let heart_bg ;
  if (post.post_liked) {
    heart_bg = "";
  } else {
    heart_bg = "-empty";
  }
  like_icon.className = `icon-heart${heart_bg} col-auto`
  
  if (document.getElementById('following')) {
    like_icon.addEventListener('click',() => count_like(post));
  } else {
    like_icon.addEventListener('click',() => force_login());
  }

  likes_row.append(like_icon);
  
  
  
  // likes amount


  const likes = document.createElement('div');
  likes.id = `likes_amount_${post.post_id}`;
  likes.className = "card-text likes col-auto ";
  likes.innerHTML = post.post_likes;
  // console.log(post.post_likes)
  likes_row.append(likes);

  const likes_text = document.createElement('div');
  likes_text.className = "card-text likes_text col-auto ";
  likes_text.innerHTML = " like";
  likes_row.append(likes_text);

  const date = document.createElement('div');
  date.className = "blockquote-footer col-auto";
  date.innerHTML = `Created date: ${post.post_created_date}`;
  // console.log(post.post_created_date)
  likes_row.append(date);

  if(post.post_editable) {
      const edit = document.createElement('button');
      edit.className = "card-text col-auto btn btn-primary";
      edit.innerHTML = "Edit";
      edit.addEventListener('click', () => edit_post(post) );
      likes_row.append(edit);
  }

  card_body.append(likes_row);    
  post_card.append(card_body);

  const row = document.createElement('div');
  row.className = "container";
  row.append(post_card);

  document.querySelector('#posts').append(row);
  // console.log('done')
//   document.querySelector('#posts').style.display = 'block'
//   document.querySelector('#posts').style.display.innerHTML="fdg";
}

function profile_page(post_creator_id){
  load_posts(`?profile=${post_creator_id}`,1);
  document.querySelector('#newPost').style.display = 'none';
  follow_btn = document.getElementById('follow-btn');
  follow_btn.style.display = 'none';
  document.querySelector('#profile').style.display = 'block';
  fetch(`/profile_page/${post_creator_id}`)
  .then(response => response.json())
  .then(profile => {
    document.getElementById('following-amount').innerHTML = profile.userdetail_following;
    document.getElementById('followers-amount').innerHTML = profile.userdetail_followers;
    document.getElementById('profile_username').innerHTML = profile.userdetail_username;
    if (profile.userdetail_follow_available){
      follow_btn.style.display = 'unset';
      if (profile.userdetail_currently_following){
        follow_btn.innerHTML = 'Unfollow';
        follow_btn.className = "btn btn-outline-danger";
      } else {
        follow_btn.innerHTML = 'Follow';
        follow_btn.className = "btn btn-outline-success"
      }
      follow_btn.addEventListener('click', () => follow(post_creator_id));
    }
  })
  window.scrollTo(0,0)
}


// pagination
function struct_paginator(addon,page,num_pages){
  page_list = document.getElementById('pagination');
  page_list.innerHTML="";

  const previous = document.createElement('li');
  if(page==1){
      previous.className = "page-item disabled";    
  } else {
      previous.className = "page-item";    
      previous.addEventListener('click', () => load_posts(addon,page-1));
  }        
  const page_previous = document.createElement('a');
  page_previous.className="page-link";

  page_previous.href="#";
  page_previous.innerHTML="Previous";
  previous.append(page_previous);    
  page_list.append(previous);
  
  for (let item=1; item<=num_pages; item++) {
      const page_num = document.createElement('li');        
      if(item==page) {
          page_num.className = "page-item active";
      } else {
          page_num.className = "page-item";    
          page_num.addEventListener('click', () => load_posts(addon,item));
      }        
      const page_a = document.createElement('a');
      page_a.className="page-link";
      page_a.href="#";
      page_a.innerHTML=item;
      page_num.append(page_a);

      page_list.append(page_num);
  }
  
  const next = document.createElement('li');        
  if(page==num_pages){
      next.className = "page-item disabled";    
  } else {
      next.className = "page-item";    
      next.addEventListener('click', () => load_posts(addon,page+1));
  }   
  const page_next = document.createElement('a');
  page_next.className="page-link"; 
  page_next.href="#";
  page_next.innerHTML="Next";
  next.append(page_next);
  page_list.append(next); 
}

// editing post,
function edit_post(post){
  // likes_row and content_ class are created by struct_post function
  const likes_row = document.getElementById(`likes_row_${post.post_id}`);
  const content = document.getElementById(`content_${post.post_id}`);

  const post_body = content.parentNode;

  const edit_btn_row = document.createElement('div');
  edit_btn_row.className = 'edit_btn_row';
// 7777777777777777777777777777777777777777777
  const save_btn = document.createElement('button');
  save_btn.type = "button"
  save_btn.className = "btn btn-primary col-auto";
  save_btn.innerHTML = "Save";
  save_btn.addEventListener('click', () => {
    const new_post = document.getElementById(`new_post_${post.post_id}`).value;
    fetch(`/new_post`, {
      method: 'PUT',
      headers : {
        'X-CSRFToken' : getCookie("csrftoken")
      }, body: body = JSON.stringify({
        post_id: post.post_id,
        new_post: new_post,
      })
    })
    .then(response => response.json())
    .then(response => {
      if (response.result){
        content.innerHTML = new_post;
      } else {
        alert ("Editing post is not saved")
      }
      edit_btn_row.remove();
      content_editable.remove();
      post_body.append(content);
      post_body.append(likes_row);
    })
  })
  // edit_btn_row.append(save_btn); moved to below near cancel button

  const content_editable = document.createElement('input');
  content_editable.id = `new_post_${post.post_id}`;
  content_editable.type = "textarea";
  content_editable.className = "form-control col-auto";
  content_editable.value = content.innerHTML;
    
    
  document.getElementById(`likes_row_${post.post_id}`).remove();
  document.getElementById(`content_${post.post_id}`).remove();
    
  edit_btn_row.append(content_editable);
  // 77777777777777777777777777777777777777
  const cancel_button = document.createElement('button');
  cancel_button.className = "btn btn-primary ml-3";
  cancel_button.type = "button";
  cancel_button.innerHTML = "Cancel";
  cancel_button.addEventListener('click', () => {
      edit_btn_row.remove();
      content_editable.remove();
      post_body.append(content);
      post_body.append(likes_row);                  
  });
  edit_btn_row.append(save_btn);
  edit_btn_row.append(cancel_button);
  post_body.appendChild(edit_btn_row);    

}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// like vs unlike toggle count()
function count_like(post){
  fetch(`/post/${post.post_id}/count_like`)
  .then(response => response.json())
  .then(response => {
    if (response.post_liked) { 
    document.getElementById(`like_icon_${post.post_id}`).className = "icon-heart col-auto";
    
  } else {
    document.getElementById(`like_icon_${post.post_id}`).className = "icon-heart-empty col-auto";
  }
  document.getElementById(`likes_amount_${post.post_id}`).innerHTML = response.count;
  })
}

function follow(post_creator_id){
  fetch(`profile_page/${post_creator_id}/follow`)
  .then(response => response.json())
  // console.log(response)
  .then(response => {
    follow_btn = document.getElementById('follow-btn');
    if (response.followable){
      follow_btn.innerHTML = "Unfollow";
    }else {
      follow_btn.innerHTML = "Follow";
    }
    document.getElementById('followers-amount').innerHTML = response.counter_follow;
  })
}
