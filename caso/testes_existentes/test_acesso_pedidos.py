"""AV3 · B1 — R4: um usuário só pode ver os próprios pedidos.

Decisão (ver descrição do PR): pedido de outro usuário responde 404 com o mesmo corpo de um
pedido inexistente, para não revelar que o id existe (evita enumerar pedidos alheios).
"""
import unittest

from miniloja import handlers

ITEM = [{"sku": "BOLA-01", "preco": 50.0, "qtd": 1}]
DONA, OUTRO = 501, 502


def criar_pedido(usuario_id):
    status, pedido = handlers.post_pedidos(usuario_id, {"itens": ITEM, "uf": "PE"})
    assert status == 201, (status, pedido)
    return pedido


class TestAcessoPedidos(unittest.TestCase):
    def test_dona_ve_o_proprio_pedido(self):
        pedido = criar_pedido(DONA)
        status, corpo = handlers.get_pedido(DONA, pedido["id"])
        self.assertEqual(status, 200)
        self.assertEqual(corpo["id"], pedido["id"])
        self.assertEqual(corpo["usuario_id"], DONA)

    def test_outro_usuario_nao_ve_pedido_alheio(self):
        # Teste negativo (R4): falha enquanto get_pedido ignorar o usuario_id.
        pedido = criar_pedido(DONA)
        status, corpo = handlers.get_pedido(OUTRO, pedido["id"])
        self.assertEqual(status, 404)
        self.assertNotIn("itens", corpo)
        self.assertNotIn("total", corpo)

    def test_pedido_alheio_e_indistinguivel_de_inexistente(self):
        pedido = criar_pedido(DONA)
        alheio = handlers.get_pedido(OUTRO, pedido["id"])
        inexistente = handlers.get_pedido(OUTRO, 999999)
        self.assertEqual(alheio, inexistente)


if __name__ == "__main__":
    unittest.main()
