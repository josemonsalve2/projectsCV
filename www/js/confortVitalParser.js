            $(".website-option").hover( 
                function() {
                    $(this).css("background-color","#999999");
                    $(this).css("font-weight","bold");
                }, function() {
                    $(this).css("background-color","#EEEEEE");
                    $(this).css("font-weight","normal");
                });
            $(".website-option").click(
                function() {
                    if ($(this).attr("id") == "exito.com")
                    {
			$("div.results").html('');
			$("div.results").append('<div class="images_results"><h1>PAGINA PRINCIPAL</h1></div>');
			$("div.results > div.images_results").append('<div class="loading"> <img src="images/loading.gif" height="42" widht="42"></img> <br /> CARGANDO ... </div>');
			$("div.results").append('<div class="table_results"><h1>SECCI&Oacute;N COLCHONES</h1></div>');
			$("div.results > div.table_results").append('<table class="matress_table"></table>');
        		$("div.results > div.table_results > table.matress_table").append('<tr> <th> Posici&oacute;n </th> <th> Nombre Producto </th> <th> Marca </th> <th> Categoria </th> <th> Menor Precio </th> <th> Descuento sin Tarjeta </th> <th> Descuento con Tarjeta </th> <th> Precio Completo </th> <th> Producto Estrella </th> <th> Tarjeta Exito </th> </tr>');
			$("div.results > div.table_results > table.matress_table").append('<tr><td colspan = "10"><div class="loading"> <img src="images/loading.gif" height="42" widht="42"></img> <br /> CARGANDO ... </div></td><tr>');
		    	$.ajax({
				url: 'http://www.monsalvediaz.com:12345/exito/fp',
				dataType: 'json',
				})
				.done (function(JsonParsed) 
				{
					$("div.results > div.images_results").html('<h1>PAGINA PRINCIPAL</h1>');
					$.each(JsonParsed, function(index,value)
						{
							var newImage = '<div class="fp_image_div" id="'+value.fileName+'"> <a href="'+value.link+'"> <img class="fp_image" src="'+value.src+'" title="'+value.fileName+'" ></img></a> <br/><span class="fp_image_location" >'+value.position+' </span> </div>';

							$("div.results > div.images_results").append(newImage);
					});
				})
				.fail(function(jqXHR, textStatus, errorThrown)
				{
					$("div.results").html('<div class="connection_error"> <p class="error_message"> <h1>ERROR DE CONEXI&Oacute;N </h1><br/> Intente de nuevo mas tarde, si el error continua, contacte al administrador <p> </div>');
				});
			
			//Matress section
		    	$.ajax({
				url: 'http://www.monsalvediaz.com:12345/exito/matress',
				dataType: 'json',
				})
				.done (function(JsonParsed) 
				{
					$("div.results > div.table_results > table.matress_table").html('');
        				$("div.results > div.table_results > table.matress_table").append('<tr> <th> Posici&oacute;n </th> <th> Nombre Producto </th> <th> Marca </th> <th> Categoria </th> <th> Menor Precio </th> <th> Descuento sin Tarjeta </th> <th> Descuento con Tarjeta </th> <th> Precio Completo </th> <th> Producto Estrella </th> <th> Tarjeta Exito </th> </tr>');
					$.each(JsonParsed, function(index,value)
						{
							var newRow = '<tr> <td> '+value.position+' </td> <td> <a target="_blank" href ="'+value.link+'" >'+value.name+' </a> </td> <td> '+value.brand+' </td> <td> '+value.category+'  </td> <td> '+value.lowerPrice+'  </td> <td> '+value.discountNonCC+'  (notCC) </td> <td> '+value.discountCC+' </td> <td> '+value.OrigPrice+' </td>  <td> '+value.exitoStar+' </td> <td> '+value.exitoCC+' </td> </tr>'
							$("div.results > div.table_results > table.matress_table").append(newRow);
					});
				})
				.fail(function(jqXHR, textStatus, errorThrown)
				{
				});

			return false;
                    }
                    else if ($(this).attr("id") == "cdiscount.com")
                    {
                    }
                    else if ($(this).attr("id") == "linio.com")
                    {
                    }
                    else
                    {
                        alert("Wrong ID!!");   
                    }
                    
                });
