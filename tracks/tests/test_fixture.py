test_tracks_query = '''
            {
                tracks {
                    id
                    title
                    description
                }
            }
            '''
login_user_query = '''
        mutation {{
  tokenAuth(username:"{username}", password:"{password}"){{
    token
  }}
}}
        '''

register_user_query = '''
            mutation {{
  createUser(email:"{email}", password:"{password}", username:"{username}"){{
    user {{
      username
      email
    }}
  }}
}}
            '''

create_track = '''
mutation {
  createTrack(title:"Not Afraid", description:"I am not afraid", url:"http://notafraid.com"){
    track{
      id
      description
    }
  }
}

'''

update_track = '''
mutation {
  updateTrack(trackId: 1, title:"Afraid", description:"I am afraid", url:"http://afraid.com"){
    track{
      id
      description
    }
  }
}

'''

delete_track = '''
mutation {
  deleteTrack(trackId: 1){
    trackId
  }
}
'''

filter_query = '''
{
  tracks(search: "Not Afraid"){
    id
    title
    likes{
      id
    }
  }
}
'''

create_like = '''
mutation {
  createLike(trackId: 1){
    track {
      id
      title
      description
      url
    }
    user {
      id
      username
      email
    }
  }
}
'''

query_likes = '''
{
  likes{
    id
    user {
      username
    }
    track {
      title
    }
  }
}
'''

create_like_ghost_track = '''
mutation {
  createLike(trackId: 10){
    track {
      id
      title
      description
      url
    }
    user {
      id
      username
      email
    }
  }
}
'''

users_query = '''
{
  users {
    id
    username
  }
}
'''
user_query = '''
{
  user(id: 1) {
    id
    username
  }
}
'''
user_ghost_query = '''
{
  user(id: 10) {
    id
    username
  }
}
'''

create_user = '''
mutation {
  createUser(email:"jackdoe@test.com", password:"philipdoe123", username:"jackdoe"){
    user {
      id
      email
    }
  }
}
'''