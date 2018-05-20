#!/bin/env python3
"""Tests for Python Language Learner ImageScraper class"""
import unittest
import image_scraper


class ImageScraperTests(unittest.TestCase):
    def test_get_opening_root_tag(self):
        """This tests getting the opening root tag of a string of html"""
        test_string = """<div id="ires"><table></table><ol></ol></div>"""
        expected_result = """<div id="ires">"""
        self.assertEqual(image_scraper._get_opening_root_tag(test_string), expected_result)

        test_string = """ < div >blah blah blah"""
        expected_result = "< div >"
        self.assertEqual(image_scraper._get_opening_root_tag(test_string), expected_result)

        with self.assertRaises(ValueError):
            image_scraper._get_opening_root_tag("something>")

        with self.assertRaises(ValueError):
            image_scraper._get_opening_root_tag("<<something>")

        with self.assertRaises(ValueError):
            image_scraper._get_opening_root_tag(">something>")

        self.assertIsNone(image_scraper._get_opening_root_tag("something"))

        test_string = """ < div id=something style=somethingelse >blah blah blah"""
        expected_result = "< div id=something style=somethingelse >"
        self.assertEqual(image_scraper._get_opening_root_tag(test_string), expected_result)

    def test_get_element_type(self):
        """This tests getting the element type, aka the first word, of a tag string"""
        test_tag = """<div id="ires">"""
        expected_result = "div"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = b"""<div id="ires">"""
        expected_result = "div"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = " < div > "
        expected_result = "div"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = b" < div > "
        expected_result = "div"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = "<p blah blah blah>"
        expected_result = "p"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = b"<p blah blah blah>"
        expected_result = "p"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = """<meta content="text/html; charset=UTF-8" http-equiv="Content-Type">"""
        expected_result = "meta"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

        test_tag = b"""<meta content="text/html; charset=UTF-8" http-equiv="Content-Type">"""
        expected_result = "meta"
        self.assertEqual(image_scraper._get_element_type(test_tag), expected_result)

    def test_get_element_id(self):
        """This tests getting the element id from a tag"""
        test_tag = """<div id="ires">"""
        expected_result = "ires"
        self.assertEqual(image_scraper._get_element_id(test_tag), expected_result)

        test_tag = """<table id="mn" border="0" cellpadding="0" cellspacing="0" style="position:relative">"""
        expected_result = "mn"
        self.assertEqual(image_scraper._get_element_id(test_tag), expected_result)

        test_tag = """<div>"""
        self.assertIsNone(image_scraper._get_element_id(test_tag))

        test_tag = """<div id='ires'>"""
        expected_result = "ires"
        self.assertEqual(image_scraper._get_element_id(test_tag), expected_result)

        test_tag = """<div id="ires" >"""
        expected_result = "ires"
        self.assertEqual(image_scraper._get_element_id(test_tag), expected_result)

        test_tag = """<div something else id="ires">"""
        expected_result = "ires"
        self.assertEqual(image_scraper._get_element_id(test_tag), expected_result)

    def test_get_root_contents(self):
        """Tests that we can extract the contents of the root element in html"""
        test_string = """<div id="ires"><table></table><ol></ol></div>"""
        expected_result = "<table></table><ol></ol>"
        self.assertEqual(image_scraper._get_root_contents(test_string), expected_result)

        test_string = """<div id="ires"><table></table></div><div><ol></ol></div>"""
        expected_result = "<table></table>"
        self.assertEqual(image_scraper._get_root_contents(test_string), expected_result)

        test_string = """<div id="ires"></div>"""
        expected_result = ""
        self.assertEqual(image_scraper._get_root_contents(test_string), expected_result)

        test_string = """<div id="ires" /><table></table><ol></ol><div></div>"""
        expected_result = None
        self.assertEqual(image_scraper._get_root_contents(test_string), expected_result)

        test_string = """<div id="ires"/><table></table><ol></ol><div></div>"""
        expected_result = None
        self.assertEqual(image_scraper._get_root_contents(test_string), expected_result)

        test_html_fn = "test_resources/mock_good_results_div.html"
        expected_div_contents_fn = "test_resources/mock_good_results_div_contents.html"
        with open(test_html_fn, "r") as test_html:
            tested_div_contents = image_scraper._get_root_contents(test_html.read())
            with open(expected_div_contents_fn, "r") as expected_div_contents:
                self.assertEqual(tested_div_contents, expected_div_contents.read())

    def test_get_elements(self):
        """Tests that we can get the top level elements of a string of html"""
        test_string = """<table></table><ol></ol>"""
        elements = image_scraper._get_elements(test_string)
        expected_type_list = ["table", "ol"]
        self.assertListEqual([element.type for element in elements], expected_type_list)

        test_string = """<div id="ires"></div>"""
        elements = image_scraper._get_elements(test_string)
        expected_type_list = ["div"]
        self.assertListEqual([element.type for element in elements], expected_type_list)

        test_string = """<div id="ires"/>"""
        elements = image_scraper._get_elements(test_string)
        expected_type_list = ["div"]
        self.assertListEqual([element.type for element in elements], expected_type_list)

        test_string = """<div id="ires"/><table></table><ol></ol><div></div>"""
        elements = image_scraper._get_elements(test_string)
        expected_type_list = ["div", "table", "ol", "div"]
        self.assertListEqual([element.type for element in elements], expected_type_list)

    def test_get_first_root_element(self):
        """This test verifies that the root element can be extracted from input html"""
        test_string = """<div id="ires"><table></table></div><div><ol></ol></div>"""
        expected_result = """<div id="ires"><table></table></div>"""
        self.assertEqual(image_scraper._get_first_root_element(test_string), expected_result)

        test_string = """<div id="ires"/><table></table><div><ol></ol></div>"""
        expected_result = """<div id="ires"/>"""
        self.assertEqual(image_scraper._get_first_root_element(test_string), expected_result)

    # TODO baparham - HtmlElements still do not handle text nodes very well. need to enhance text node support.
    # def test_html_element(self):
    #     """This test case is meant to test the basic instantiation of an HtmlElement"""
    #     test_html_fn = "test_resources/mock_good_results_div.html"
    #     test_div_contents_fn = "test_resources/mock_good_results_div_contents.html"
    #     with open(test_html_fn, "r") as test_html:
    #         element = image_scraper.HtmlElement(test_html.read())
    #         self.assertIsInstance(element, image_scraper.HtmlElement)
    #         self.assertEqual(element.type, "div")
    #         self.assertEqual(element.id, "ires")
    #         self.assertEqual(element.num_children, 2)
    #         with open(test_div_contents_fn, "r") as test_div_contents:
    #             self.assertEqual(element.contents, test_div_contents.read())

    @unittest.skip("Descendants not properly implemented yet")
    def test_html_element_descendants(self):
        """Tests that we can get a list of descendants of an html element"""
        test_html_fn = "test_resources/mock_good_results_div.html"
        with open(test_html_fn, "r") as test_html:
            element = image_scraper.HtmlElement(test_html.read())
            descendants = element.get_descendants(tag_type="td")
            expected_descendants = [
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=http://conceptodefinicion.de/hombre/&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IFjAA&amp;usg=AOvVaw3ILwCa88kubbPQRCiK56VS"><img height="103" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0AfsT7skEL4okSp_DqbPCW4f5ucUqwvMeVU2SNpqG6ZxhFirWIQBYUwg" width="137" alt="Resultado de imagen para hombre"></a><br><cite title="conceptodefinicion.de">conceptodefinicion.de</cite><br>Qué es <b>Hombre</b>? - Su Definición, Concepto y Significado<br>645 × 485 - 76 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://www.elcorteingles.es/moda/A20672140-traje-de-hombre-dustin-liso-negro/&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IGDAB&amp;usg=AOvVaw0hYom__9MLhYEDag12P7c5"><img height="137" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIVin2tbOCsLBM3Rt9oisJVkcQ6HJi9erSDZi4GFCl5UQkOYbsMCxcrBM" width="110" alt="Resultado de imagen para hombre"></a><br><cite title="elcorteingles.es">elcorteingles.es</cite><br>Traje de <b>hombre</b> Dustin liso negro · Dustin · Moda · El Corte Inglés<br>516 × 640 - 34 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://www.elcorteingles.es/moda/A9943697-traje-de-hombre-dustin/&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IGjAC&amp;usg=AOvVaw2-e2f8hg5l9wYt1SbUb1uQ"><img height="137" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_Bbtzl7l4sjBpSzs-sdFV5Gdwd0xi4nI3BDkJ4nU1Qny8LjvGb4t0yQYS" width="110" alt="Resultado de imagen para hombre"></a><br><cite title="elcorteingles.es">elcorteingles.es</cite><br>Traje de <b>hombre</b> Dustin · Dustin · Moda · El Corte Inglés<br>516 × 640 - 29 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://www.fashionspark.com/hombre/9453-jeans-hombre-101-skinny.html&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IHDAD&amp;usg=AOvVaw06ebllR4lOQU59Fgm_A_oY"><img height="127" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGK7gRyhGjU7rBI2os8pErlyGBWkaWpq2sT90KNTE1qGupCHZDQeWV2d8" width="85" alt="Resultado de imagen para hombre"></a><br><cite title="fashionspark.com">fashionspark.com</cite><br>Jeans <b>Hombre</b> 101 Skinny - Fashion's Park Tienda Online<br>300 × 450 - 16 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=http://latam.askmen.com/tips-de-estilo/7863/article/el-look-2017-para-el-hombre-de-ciudad&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IHjAE&amp;usg=AOvVaw38wimqN0xxwc3OXKnN_X5k"><img height="83" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8nNezCwLlFVeIO0RVSTJP6XkLHq4HGxmoY72YQOmDoj1MfQIU41ZT40I" width="150" alt="Resultado de imagen para hombre"></a><br><cite title="latam.askmen.com">latam.askmen.com</cite><br>look 2017 para el <b>hombre</b> de ciudad - Tips de estilo<br>1210 × 666 - 717 k&nbsp;-&nbsp;png</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=http://www.salud180.com/salud-dia-dia/asi-es-el-hombre-ideal-segun-la-ciencia&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IIDAF&amp;usg=AOvVaw0DGw9NY8YHPMn-MtedlXbW"><img height="82" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrUA67pKmBr9PXd5997ez0cA4ttHCsrH-vSt9I60gHV4UWV7Cv6bUJ9dOD" width="135" alt="Resultado de imagen para hombre"></a><br><cite title="salud180.com">salud180.com</cite><br>Así es el <b>hombre</b> ideal según la ciencia | Salud180<br>600 × 364 - 21 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://www.venca.es/p/013047/camiseta-de-hombre-basica-lisa-con-doble-pespunte-en-el-cuello&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IIjAG&amp;usg=AOvVaw0Ft4nS3a1jxb3RXH225GHS"><img height="143" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpWqVeOpu-Dx-Rnr57RgX0UBShdUQF1A66tHx0t6VdO1sMKtQ8BcjaShQ" width="107" alt="Resultado de imagen para hombre"></a><br><cite title="venca.es">venca.es</cite><br>Camiseta de <b>hombre</b> básica lisa con doble pespunte en el cuello ...<br>591 × 791 - 36 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://fiftyfactory.com/es/es/hombre&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IJDAH&amp;usg=AOvVaw3PH9Zg93w1fMkDWGqak5Vt"><img height="146" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoP9ceEyssfStg642p5s-w_WCWrxkrsVpfc7Nrin79QBgtFHFhu0GQbpVT" width="97" alt="Resultado de imagen para hombre"></a><br><cite title="fiftyfactory.com">fiftyfactory.com</cite><br>Outlet Ropa de <b>Hombre</b> | Fifty Factory<br>600 × 900 - 100 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://www.montagneoutdoors.com.ar/es/producto/1939-buzo-de-hombre-byron&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IJjAI&amp;usg=AOvVaw3Koao3K1Dpnd0qjj1bkuBV"><img height="150" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSojQRUJURj01_qoK2BpiXMDjF9uqvE_-Ll-ebZEAva9fYiM4sr8c86YWtsDg" width="150" alt="Resultado de imagen para hombre"></a><br><cite title="montagneoutdoors.com.ar">montagneoutdoors.com.ar</cite><br>Buzo de <b>hombre</b> Byron<br>1200 × 1200 - 288 k&nbsp;-&nbsp;jpg</td>"""),
                image_scraper.HtmlElement("""<td style="width:25%;word-wrap:break-word"><a href="/url?q=https://www.montagneoutdoors.com.ar/es/producto/102-campera-de-hombre-ivory&amp;sa=U&amp;ved=0ahUKEwi32prIy4vbAhXJ5oMKHQtKDeMQwW4IKDAJ&amp;usg=AOvVaw3B48FY_kME9GCIGGu7kun-"><img height="150" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyk8_649n61ucOBix-iBVdb9Hk-bms6L2QmaADCWatgrJD0l2l0AtuDaTe" width="150" alt="Resultado de imagen para hombre"></a><br><cite title="montagneoutdoors.com.ar">montagneoutdoors.com.ar</cite><br>Montagne: camperas, campera, camperas <b>hombres</b>, camperas de ...<br>1200 × 1200 - 221 k&nbsp;-&nbsp;jpg</td>"""),
            ]
            for array_index in range(len(expected_descendants)):
                self.assertEqual(descendants[array_index].type, expected_descendants[array_index].type)
                self.assertEqual(descendants[array_index].id, expected_descendants[array_index].id)
                self.assertEqual(descendants[array_index].num_children, expected_descendants[array_index].num_children)
                self.assertEqual(descendants[array_index].contents, expected_descendants[array_index].contents)

    @unittest.skip("Not implemeted yet")
    def test_get_matching_descendants(self):
        """Tests that we can extract a list of matching descendants from an HtmlElement"""
        pass

    #
    # def test_extract_results_div(self):
    #     """This test tests that we can extract the correct results div from a string of html"""
    #     mock_html_filename = "test_resources/mock_good_html_file.html"
    #     mock_results_div_filename = "test_resources/mock_good_results_div.html"
    #     with open(mock_html_filename, "r") as html_input:
    #         html_string = html_input.read()
    #         tested_results_div = image_scraper._extract_results_div(html_string)
    #         with open(mock_results_div_filename, "rb") as mock_res_div:
    #             self.assertEqual(mock_res_div.read(), tested_results_div)


if __name__ == '__main__':
    unittest.main()
