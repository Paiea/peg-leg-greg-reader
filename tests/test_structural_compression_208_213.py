import unittest

from scripts.apply_structural_compression_208_213 import apply_transformations


class BrenSequenceCompressionTest(unittest.TestCase):
    def test_compresses_repeated_pressure_without_losing_evidence_spine(self):
        docs = {
            208: '<article class="prose"><p>I woke because someone hit wood outside.</p><p>OLD WAKEUP AND CHECKS</p><p>At the hall, the front door was locked.</p><p>Before house, Rinna made us check the things that could actually cost money.</p><p>OLD INSPECTION LOOP</p><p>That was the entire council.</p><p>Guild man rumor survives.</p></article>',
            209: '<article class="prose"><p>There was still no note under the cup.</p><p>OLD MORNING LOOP</p><p>At the hall, the front door was latched again.</p><p>Then she said, "The man might be called Bren."</p><p>Same words. Cart yard. Small share. Wheels.</p><p>Rinna folded the scrap with Bren\'s possible name and put it beneath the edge of her ledger.</p><p>OLD QUALIFICATION LOOP</p><p>The board was already up.</p><p>Broken lamp rumor survives.</p></article>',
            210: '<article class="prose"><p>The handcart was missing a wheel.</p><p>Pin pulled. Not broken. Keep all this evidence.</p><p>The cart came inside twenty minutes later.</p><p>OLD TABLE CART PROP LOGISTICS</p><p>House opened.</p><p>Later unique theatre material.</p></article>',
            211: '<article class="prose"><p>Talla works at the cart yard.</p><p>Bren. Left glove. Small share. Paid once. More.</p><p>The door closed.</p><p>I looked at Rinna.</p><p>OLD QUESTION BY QUESTION UNKNOWN LOOP</p><p>Rinna waited.</p><p>I sighed.</p><p>"Fine."</p><p>"Good."</p><p>"Everybody uses that word too much."</p><p>The board said:</p><p>Work continues.</p></article>',
            212: '<a rel="prev" href="211.html">Chapter 211</a><a rel="next" href="213.html">Chapter 213</a><article class="prose"><p>Antonius Vale found me before breakfast.</p><p>Vale note. Tomorrow first bell. Two copper debt work setup.</p><p>Ordinary theatre day and false alarm.</p></article>',
            213: '<a rel="prev" href="212.html">Chapter 212</a><article class="prose"><p>Antonius sent a cart.</p><p>OLD ACCOUNTING PROCEDURE</p><p>The work was exactly what the note had promised.</p><p>More accounting.</p><p>Then I reached a receiving sheet marked for a yard near Mason\'s Cut.</p><p>Vale hears Bren facts.</p><p>"The first amount tests whether payment is easier than refusal."</p><p>Later Hessa material.</p></article>',
        }
        once = apply_transformations(docs)
        twice = apply_transformations(once)
        self.assertEqual(once, twice)
        self.assertIn('STRUCTURAL-COMPRESSION-208-213:208', once[208])
        self.assertNotIn('OLD INSPECTION LOOP', once[208])
        self.assertIn('STRUCTURAL-COMPRESSION-208-213:209', once[209])
        self.assertNotIn('OLD QUALIFICATION LOOP', once[209])
        self.assertIn('Pin pulled. Not broken.', once[210])
        self.assertNotIn('OLD TABLE CART PROP LOGISTICS', once[210])
        self.assertIn('Bren. Left glove. Small share. Paid once. More.', once[211])
        self.assertNotIn('OLD QUESTION BY QUESTION UNKNOWN LOOP', once[211])
        self.assertIn('data-structural-status="merged"', once[212])
        self.assertIn('href="213.html"', once[211])
        self.assertIn('href="211.html"', once[213])
        self.assertIn('Vale had sent for me before breakfast', once[213])
        self.assertIn('first amount tests whether payment is easier than refusal', once[213])


if __name__ == '__main__':
    unittest.main()
