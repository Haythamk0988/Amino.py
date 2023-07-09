def create_frame(self, community_id, title, image_url):
    payload = {
        'title': title,
        'image_url': image_url
    }
    endpoint = f"/x{community_id}/s/frame/create"
    response = self.session.post(endpoint, json=payload)
    return response.json()
