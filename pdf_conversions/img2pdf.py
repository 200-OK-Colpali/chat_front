from PIL import Image  


images = [
    Image.open("test_files/" + f)
    for f in ["img1.jpg", "img2.jpeg", "img3.png"]
]

pdf_path = "done.pdf"
    
images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)