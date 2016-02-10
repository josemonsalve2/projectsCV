#!/usr/bin/python3.4
from collections import namedtuple
import requests as req
from bs4 import BeautifulSoup as bs


#struct for the results 
Img=namedtuple("Img","src link fileName position")
Product=namedtuple("Product","name brand category lowerPrice discountNonCC discountCC OrigPrice position link imgSrc exitoStar exitoCC")


def parse_exito_fp(url_exito):
    """Parse Exito.com front page lookig for images
    We know that exito uses images to show the content of the website in the front page
    to date there are two possible places to put the images. One is a carousel, which 
    has been changed in the past. The other one is in the list. The idea is to return an structure that
    contains a list of structures containin the image, its link, name, and position (carousel or mosaic)
    """
    #Request to the website
    exito_req = req.get(url_exito)

    #Using Beautiful soup to obtain the website structure
    exito_soup = bs(exito_req.content,"html.parser")
    
    #Makin sure the search returned anything
    if (exito_soup is None):
        print("[WARNING] soup failed\n")
        return None
    
    exito_soup_content = exito_soup.find("div",{"class":"row-fluidbg"})
    #Makin sure the search returned anything
    if (exito_soup_content is None):
        print("[WARNING] row-fluidbg failed\n")
        return None
    
    #Makin sure the search returned anything
    exito_soup_content_carousel = exito_soup_content.find("div",{"class":"row-fluid newCarruselPpal"})
    if (exito_soup_content_carousel is None):
        print ("[WARNING] Carousel not found\n")
    
    #Find the information of the front page banners and the 
    #carousel.
    divs_front_page = exito_soup_content.find_all("div",attrs={"class":"itemDH box"})
    
    #Makin sure the search returned anything
    if (divs_front_page is None):
        print ("[WARNING itemDH box not fount\n]")
        return None

    info_exito_fp=[]

    #Obtaining the carrusel images
    if (exito_soup_content_carousel is not None):
        for img in exito_soup_content_carousel.find_all("img"):
            thisImgSrc="https://www.exito.com"+img["src"]
            thisImgLink="https://www.exito.com"+img.find_parent("a")["href"]
            thisImgFileName=thisImgSrc.split("/")[-1]
            thisImgPosition="Carrusel"
            newImg=Img(src = thisImgSrc, link = thisImgLink, fileName=thisImgFileName, position = thisImgPosition)
            info_exito_fp.append(newImg);
    #Endif carousel 
    
    #Obtaining the front page banners
    for div in divs_front_page:
        thisImg=div.find("img")
        thisImgSrc="https://www.exito.com"+thisImg["src"]
        thisImgLink="https://www.exito.com"+thisImg.find_parent("a")["href"]
        thisImgFileName=thisImgSrc.split("/")[-1]
        thisImgPosition="Mosaico"
        newImg=Img(src = thisImgSrc, link = thisImgLink, fileName=thisImgFileName, position = thisImgPosition)
        info_exito_fp.append(newImg);
   
    return info_exito_fp
#Enddef parse_exito_fp

def convertPrice(priceStr):
    """This function translates the string price with all the garbage caracters to a float
    """
    for ch in [' ','.','$',',','\n','\t']:
        if ch in priceStr:
            priceStr=priceStr.replace(ch,"")
    return float(priceStr)
#enddef convertPrice


def parse_exito_matress(url_exito_matress):
    """ Parse Exito.com the matress section. It goes an generates a table with the information of all the matress that are being sold and 
    This information is: 
        Name
        Brand
        category
        LowerPrice
        Discount (notCC)
        Discount (CC)
        fullPrice
        page
        Link
        ImageSrc
        Exito StartProduct (yes/no)
        Exito CC (yes/no)
    """
    #result to return  
    resultProducts = []

    #Request to the website
    exito_req = req.get(url_exito_matress)

    #Using Beautiful soup to obtain the website structure
    exito_soup = bs(exito_req.content,"html.parser")
    
    #Makin sure the search returned anything
    if (exito_soup is None):
        return None

    #Getting number of products
    items_per_page=80
    num_results_content_box = exito_soup.find("div",attrs={"class":"plpPaginationTop row-fluid box"})
    #Makin sure the search returned anything
    if (num_results_content_box is None):
        return None
    num_results_content = num_results_content_box.find("div",attrs={"class":"pull-left"})
    #Makin sure the search returned anything
    if (num_results_content is None):
        return None
    num_results_content = num_results_content.contents
    
    num_results= int(str(num_results_content).split(" ")[5])
    num_pages = num_results//items_per_page
    if (num_results%items_per_page != 0):
        num_pages = num_pages + 1 
    #endif
    
    #for each page, we gotta go and grab the info
    cnt_num_pages=num_pages
    
    while (cnt_num_pages != 0):
        #the url changes per page we get the request again
        url = url_exito_matress+"?No="+str((num_pages-cnt_num_pages)*items_per_page)+"&Nrpp="+str(items_per_page)
        exito_req = req.get(url)

        #Using Beautiful soup to obtain the website structure
        exito_soup = bs(exito_req.content,"html.parser")
        #Makin sure the search returned anything
        if (exito_soup is None):
            return None
        
        exito_soup_products = exito_soup.find("div",attrs={"id":"plpContent"})
        #Makin sure the search returned anything
        if (exito_soup_products is None):
            return None

        exito_soup_products = exito_soup_products.find_all("div",attrs={"class":"technology smallProduct"})
        #Makin sure the search returned anything
        if (exito_soup_products is None):
            return None

        #Iterate over each product and get the info
        for product in exito_soup_products:
            if (product.find("div",attrs={"class","productAvailable"}) is None):
                #If product is available
                #Getting name
                productName = product.find("div",attrs={"class":"productBrand box"}).find("a")["title"]
                #Getting brand
                productBrand = product.find("div",attrs={"class":"productBrand box"}).find("h3").contents
                #Getting product Category
                productCategory = product["data-categoryparent"]
                #Getting is product Exitostar
                if (product.find("div",attrs={"class":"pro-Estrella Tarjeta"}) is not None):
                    productExitoStar = True
                else:
                    productExitoStar = False
                #Getting product prices and discounts
                productLowerPrice=0
                productBefore=0
                productCCDiscount=0
                productNonCCDiscount=0
                productExitoCC=False
                if product.find("a",attrs={"class":"productPrice box"}).find("h4",attrs={"class","price"}) is None:
                    #if product has an offer
                    productPriceOffer=product.find("a",attrs={"class":"productPrice box"}).find("h4",attrs={"class","priceOffer"})
                    productPriceBefore=product.find("a",attrs={"class":"productPrice box"}).find("h6",attrs={"class","before"})
                    if (productPriceOffer is not None):
                        #if product does not have offer nor normal price, they don't have it but it is listed
    
                        #Getting product prices
                        productLowerPrice = convertPrice(str(productPriceOffer.contents[0]))
                        productBefore = convertPrice(str(productPriceBefore.find("span").contents[0]))
    
                        #Does it have ExitoCC special discount?
                        if (productPriceOffer.find("img",attrs={"class":"iconPaymentCard"}) is not None):
                            productExitoCC=True
                            productOtherPayment = convertPrice(str(product.find("a",attrs={"class":"productPrice box"}).find("h5",attrs={"class","otherMedia"}).find("span").contents[0]))
                            productCCDiscount = 1 - productLowerPrice/productBefore
                            productNonCCDiscount = 1 - productLowerPrice/productOtherPayment
                        else:
                            ProductExitoCC = False
                            productCCDiscount = 0
                            productNonCCDiscount = 1 - productLowerPrice/productBefore
                        #endif
                    #endif
                else:
                    #Product not on sale
                    productLowerPrice=convertPrice(str(product.find("a",attrs={"class":"productPrice box"}).find("h4",attrs={"class","price"}).contents[0]))
                    productBefore=productLowerPrice
                    
    
                #endif
                
                #getting the product position
                productPosition = product["data-position"]
                #Getting the link
                productLink = "https://www.exito.com"+str(product.find("div",attrs={"class":"productBrand box"}).find("a")["href"])
                #Getting the ImgSrc
                productImgSrc = "https://www.exito.com"+str(product.find("div",attrs={"class":"productImage"}).find("img")["src"])
                
                newProduct = Product(name =productName, brand = productBrand, category = productCategory, lowerPrice = productLowerPrice, discountNonCC = productNonCCDiscount, discountCC = productCCDiscount, OrigPrice = productBefore, position = productPosition, link = productLink, imgSrc = productImgSrc, exitoStar = productExitoStar, exitoCC = productExitoCC)

                resultProducts.append(newProduct)
            #endif product available
        #endfor

        #counter of the while loop
        cnt_num_pages = cnt_num_pages - 1
    #endwhile
    
    return resultProducts
#Enddef parse_exito_matress
    

