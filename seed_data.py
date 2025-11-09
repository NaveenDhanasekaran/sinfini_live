import requests
from database import get_db
from models import Product, BlogPost, GalleryItem
import os

def download_image(url, filename):
    """Download image from URL and save to uploads folder"""
    try:
        # Add headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=15, headers=headers)
        if response.status_code == 200:
            filepath = os.path.join('uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return f'/uploads/{filename}'
        else:
            print(f"  ⚠️  Failed to download (status {response.status_code}): {filename}")
    except Exception as e:
        print(f"  ⚠️  Error downloading {filename}: {e}")
    return None

def seed_products():
    """Add sample products with images"""
    db = get_db()
    
    print("Adding sample products...")
    
    products = [
        {
            'name': 'Premium Cotton Fabric - White',
            'category': 'Cotton Fabrics',
            'description': 'High-quality 100% pure cotton fabric, perfect for garments and home textiles. Soft, breathable, and durable. Ideal for shirts, dresses, and bedding. Available in bulk quantities for international export.',
            'image': 'https://images.unsplash.com/photo-1558769132-cb1aea1f1f57?w=800&q=80'
        },
        {
            'name': 'Synthetic Polyester Blend',
            'category': 'Synthetic Fabrics',
            'description': 'Premium polyester blend fabric with excellent durability and wrinkle resistance. Perfect for modern garments, sportswear, and industrial applications. Quick-drying and easy to maintain.',
            'image': 'https://images.unsplash.com/photo-1626497764552-8032d8d6e2f9?w=800&q=80'
        },
        {
            'name': 'Elegant Ladies Dress Collection',
            'category': 'Garments',
            'description': 'Beautiful collection of ladies dresses featuring premium fabrics and contemporary designs. Perfect for retail and boutique buyers. Available in various sizes and colors. Exported to markets across Asia, Africa, and Europe.',
            'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80'
        },
        {
            'name': 'Luxury Bed Linen Set',
            'category': 'Linens',
            'description': 'Premium quality bed linen sets crafted from the finest cotton. Includes fitted sheets, flat sheets, and pillowcases. Ultra-soft with high thread count. Perfect for hotels and homes seeking luxury comfort.',
            'image': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80'
        },
        {
            'name': 'Terry Towel Collection',
            'category': 'Terry Toweling',
            'description': 'Soft and absorbent terry towels made from premium cotton. Available in bath towels, hand towels, and face towels. Perfect for hospitality industry and retail. Durable and long-lasting with excellent color retention.',
            'image': 'https://images.unsplash.com/photo-1604696980386-c589383f0e0a?w=800&q=80'
        },
        {
            'name': 'Printed Cotton Fabric - Floral',
            'category': 'Cotton Fabrics',
            'description': 'Beautiful floral printed cotton fabric, ideal for ladies garments and home décor. Vibrant colors and intricate patterns. Pre-washed and shrink-resistant. Perfect for fashion designers and manufacturers.',
            'image': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&q=80'
        },
        {
            'name': 'Performance Athletic Fabric',
            'category': 'Synthetic Fabrics',
            'description': 'High-performance synthetic fabric designed for athletic wear. Moisture-wicking, breathable, and stretchable. Perfect for sportswear manufacturers. UV protection and anti-bacterial properties included.',
            'image': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&q=80'
        },
        {
            'name': 'Traditional Embroidered Garments',
            'category': 'Garments',
            'description': 'Exquisite collection of traditionally embroidered ladies garments. Handcrafted details with modern silhouettes. Premium fabrics with intricate embroidery work. Perfect for special occasions and festive wear.',
            'image': 'https://images.unsplash.com/photo-1617019114583-affb34d1b3cd?w=800&q=80'
        },
        {
            'name': 'Table Linen Collection',
            'category': 'Linens',
            'description': 'Elegant table linen collection including tablecloths, napkins, and runners. Made from high-quality cotton and linen blends. Perfect for restaurants, hotels, and home dining. Available in multiple colors and sizes.',
            'image': 'https://images.unsplash.com/photo-1607643147229-1cc4c249711b?w=800&q=80'
        },
        {
            'name': 'Bamboo Terry Towels - Eco-Friendly',
            'category': 'Terry Toweling',
            'description': 'Eco-friendly bamboo terry towels combining sustainability with luxury. Super soft, highly absorbent, and naturally antibacterial. Perfect for environmentally conscious buyers. Biodegradable and renewable material.',
            'image': 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&q=80'
        },
        {
            'name': 'Premium Denim Fabric',
            'category': 'Cotton Fabrics',
            'description': 'High-quality denim fabric perfect for jeans, jackets, and accessories. Durable weave with excellent color fastness. Available in various weights and washes. Ideal for fashion brands and garment manufacturers.',
            'image': 'https://images.unsplash.com/photo-1582552938357-32b906d55af5?w=800&q=80'
        },
        {
            'name': 'Silk Blend Evening Fabric',
            'category': 'Synthetic Fabrics',
            'description': 'Luxurious silk blend fabric with beautiful drape and sheen. Perfect for evening wear, formal dresses, and special occasion garments. Combines the elegance of silk with the durability of synthetic fibers.',
            'image': 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80'
        }
    ]
    
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads/products', exist_ok=True)
    
    for idx, product_data in enumerate(products):
        print(f"Adding product {idx + 1}/{len(products)}: {product_data['name']}")
        
        # Download image
        image_filename = f"products/product_{idx + 1}.jpg"
        image_url = download_image(product_data['image'], image_filename)
        
        if not image_url:
            print(f"  ⚠️  Creating product without image")
        
        # Create product (image_url can be None)
        Product.create(
            db,
            name=product_data['name'],
            category=product_data['category'],
            description=product_data['description'],
            image_url=image_url
        )
    
    print(f"✅ Successfully added {len(products)} products!")

def seed_blog_posts():
    """Add sample blog posts"""
    db = get_db()
    
    print("\nAdding sample blog posts...")
    
    posts = [
        {
            'title': 'The Future of Textile Exports in UAE',
            'content': '''<h2>Leading the Way in Global Textile Trade</h2>
            <p>The United Arab Emirates has emerged as a major hub for textile exports, connecting manufacturers with global markets. At Sinfini Marketing FZC, we're proud to be part of this dynamic industry.</p>
            
            <h3>Why UAE for Textile Exports?</h3>
            <p>The strategic location of the UAE provides unparalleled access to markets across Asia, Africa, and Europe. Our state-of-the-art logistics infrastructure ensures timely delivery of premium quality textiles to our international partners.</p>
            
            <h3>Quality Standards</h3>
            <p>We maintain the highest quality standards in all our products, from cotton fabrics to terry toweling. Every product undergoes rigorous quality checks before export.</p>
            
            <p>Our commitment to excellence has made us a trusted partner for businesses worldwide. We look forward to serving the growing global demand for premium textiles.</p>''',
            'author': 'Sinfini Marketing Team',
            'image': 'https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?w=800&q=80'
        },
        {
            'title': 'Sustainable Textiles: Our Commitment to the Environment',
            'content': '''<h2>Eco-Friendly Textile Solutions</h2>
            <p>Sustainability is not just a trend—it's a responsibility. At Sinfini Marketing FZC, we're committed to providing eco-friendly textile solutions that don't compromise on quality.</p>
            
            <h3>Sustainable Materials</h3>
            <p>We offer a range of sustainable fabric options including organic cotton, bamboo fiber, and recycled polyester. These materials provide the same quality and durability as traditional fabrics while reducing environmental impact.</p>
            
            <h3>Ethical Manufacturing</h3>
            <p>All our products are sourced from manufacturers who follow ethical labor practices and environmental regulations. We believe in creating value for all stakeholders in our supply chain.</p>
            
            <p>Join us in building a more sustainable future for the textile industry.</p>''',
            'author': 'Environmental Team',
            'image': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800&q=80'
        },
        {
            'title': 'Cotton vs Synthetic: Choosing the Right Fabric',
            'content': '''<h2>Understanding Fabric Types</h2>
            <p>Choosing between cotton and synthetic fabrics depends on your specific needs. Let's explore the benefits of each to help you make an informed decision.</p>
            
            <h3>Natural Cotton Benefits</h3>
            <ul>
                <li>Breathable and comfortable</li>
                <li>Hypoallergenic and skin-friendly</li>
                <li>Biodegradable and eco-friendly</li>
                <li>Excellent for hot climates</li>
            </ul>
            
            <h3>Synthetic Fabric Advantages</h3>
            <ul>
                <li>Durable and long-lasting</li>
                <li>Wrinkle-resistant</li>
                <li>Quick-drying properties</li>
                <li>Cost-effective for large orders</li>
            </ul>
            
            <p>At Sinfini Marketing, we offer both options to meet diverse customer needs. Our experts can help you choose the perfect fabric for your requirements.</p>''',
            'author': 'Product Specialist',
            'image': 'https://images.unsplash.com/photo-1558769132-cb1aea1f1f57?w=800&q=80'
        }
    ]
    
    for idx, post_data in enumerate(posts):
        print(f"Adding blog post {idx + 1}/{len(posts)}: {post_data['title']}")
        
        # Download image
        image_filename = f"blog/blog_{idx + 1}.jpg"
        image_url = download_image(post_data['image'], image_filename)
        
        if not image_url:
            print(f"  ⚠️  Creating blog post without image")
        
        # Create blog post (image_url can be None)
        BlogPost.create(
            db,
            title=post_data['title'],
            content=post_data['content'],
            author=post_data['author'],
            image_url=image_url
        )
    
    print(f"✅ Successfully added {len(posts)} blog posts!")

def seed_gallery():
    """Add sample gallery items"""
    db = get_db()
    
    print("\nAdding sample gallery items...")
    
    gallery_items = [
        {
            'type': 'image',
            'url': 'https://images.unsplash.com/photo-1558769132-cb1aea1f1f57?w=800&q=80',
            'title': 'Premium Cotton Fabrics',
            'description': 'Our collection of premium cotton fabrics'
        },
        {
            'type': 'image',
            'url': 'https://images.unsplash.com/photo-1626497764552-8032d8d6e2f9?w=800&q=80',
            'title': 'Fabric Manufacturing',
            'description': 'State-of-the-art fabric production'
        },
        {
            'type': 'image',
            'url': 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=800&q=80',
            'title': 'Warehouse Facilities',
            'description': 'Our modern storage and distribution center'
        },
        {
            'type': 'image',
            'url': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&q=80',
            'title': 'Colorful Textile Range',
            'description': 'Wide variety of colors and patterns'
        },
        {
            'type': 'image',
            'url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800&q=80',
            'title': 'Fashion Garments',
            'description': 'Ready-to-wear ladies garments'
        },
        {
            'type': 'image',
            'url': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80',
            'title': 'Luxury Bedding',
            'description': 'Premium bed linen collection'
        }
    ]
    
    os.makedirs('uploads/gallery', exist_ok=True)
    
    added_count = 0
    for idx, item_data in enumerate(gallery_items):
        print(f"Adding gallery item {idx + 1}/{len(gallery_items)}: {item_data['title']}")
        
        # Download image
        image_filename = f"gallery/gallery_{idx + 1}.jpg"
        media_url = download_image(item_data['url'], image_filename)
        
        # Only create if download was successful
        if media_url:
            GalleryItem.create(
                db,
                media_type=item_data['type'],
                media_url=media_url,
                title=item_data['title'],
                description=item_data['description']
            )
            added_count += 1
        else:
            print(f"  ⚠️  Skipping gallery item due to download failure")
    
    print(f"✅ Successfully added {added_count}/{len(gallery_items)} gallery items!")

if __name__ == '__main__':
    print("🌱 Seeding database with sample data...\n")
    seed_products()
    seed_blog_posts()
    seed_gallery()
    print("\n🎉 Database seeding completed successfully!")
    print("\nYou can now:")
    print("1. Start the backend: python app.py")
    print("2. Start the frontend: cd ../frontend && npm start")
    print("3. Visit: http://localhost:3000")
