class rbnode(object):
    """
    A node in a red black tree.
    """

    def __init__(self, key):
        "Construct."
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        "String representation."
        return str(self.key)


    def __repr__(self):
        "String representation."
        return str(self.key)


class rbtree(object):
    """
    A red black tree.
    """


    def __init__(self, create_node=rbnode):
        "Construct."

        self._nil = create_node(key=None)
        "Our nil node, used for all leaves."

        self._root = self.nil
        "The root of the tree."

        self._create_node = create_node
        "A callable that creates a node."


    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")


    def search(self, key, x=None):
        """
        Search the subtree rooted at x (or the root if not given) iteratively for the key.

        @return: self.nil if it cannot find it.
        """
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x


    def minimum(self, x=None):
        """
        @return: The minimum value in the subtree rooted at x.
        """
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x


    def maximum(self, x=None):
        """
        @return: The maximum value in the subtree rooted at x.
        """
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def delete_key(self, key):
        "Find the node that contains the key"
        z = self.search(key)
        assert (self.nil != z) , "Key to be deleted not found!"
        if self.root == z and (z.left == self.nil and z.right == self.nil):
            self._root = self.nil
        elif z.left == self.nil and z.right != self.nil:
            if z.red == True:
                z._right._red = True
            else:
                z._right._red = False
                z._p._right = z._right
        else:
            self.delete_node(z)

    def delete_node(self, z):
        "Delete the node z from the tree"
        if z._left != self.nil:
            leaf = self.maximum(z._left)
            z._key,leaf._key = leaf._key,z._key
        else:
            leaf = z
        x = leaf.p
        if leaf._red == True:
            if leaf._p._right == leaf:
                leaf._p._right = self.nil
            else:
                leaf._p._left = self.nil
        else:
            if leaf._p._right == leaf:
                leaf._p._right = self.nil
                self._delete_fixup(x,leaf._p._right)
            else:
                leaf._p._left = self.nil
                self._delete_fixup(x,leaf._p._left)
        if self.root.left == self.nil and self.root.right != self.nil:
            self._root._right._red = True
        if self.root.right == self.nil and self.root.left != self.nil:
            self._root._left._red = True


    def _delete_fixup(self, x, r):
        """Restore Red-Black properties after delete"""
        color = x.red
        if x.right == r:
            y = x._left
        else:
            y = x._right
        if y.red == True:
            if y == x.left:
                self._right_rotate(x)
            if y == x.right:
                self._left_rotate(x)
            y._red = False
            x._red = True
            self._delete_fixup(x,r)
        elif y.red == False and (y.left.red == True or y.right.red == True):
            if y.left == self.nil and y.right == self.nil:
                y._red = True
                if x.red == True:
                    x._red = False
                else:
                    self._delete_fixup(x.p,x)
            elif  y.left.red == False and y.right.red == False:
                y._red = True
                if x.red == True:
                    x._red = False
                else:
                    self._delete_fixup(x.p,x)
            else:
                if y == x.left:
                    if y.right == self.nil:
                        self._right_rotate(y)
                        y._red = color
                        x._red = False
                        y._left._red = False
                    else:
                        self._left_rotate(y)
                        self._right_rotate(x)
                        y._right._red = color
                        y._red = False
                        x._red = False
                if y == x.right:
                    if y.left == self.nil:
                        self._left_rotate(x)
                        y._red = color
                        x._red = False
                        y._right._red = False
                    else:
                        self._right_rotate(y)
                        self._left_rotate(x)
                        y._left._red = color
                        y._red = False
                        x._red = False
        self.root._red = False


    def insert_key(self, key):
        "Insert the key into the tree."
        self.insert_node(self._create_node(key=key))


    def insert_node(self, z):
        "Insert node z into the tree."
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)


    def _insert_fixup(self, z):
        "Restore red-black properties after insert."
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False


    def _left_rotate(self, x):
        "Left rotate x."
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        "Left rotate y."
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x


    def check_invariants(self):
        "@return: True iff satisfies all criteria to be red-black tree."

        def is_red_black_node(node):
            "@return: num_black"
            # check has _left and _right or neither
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            # check leaves are black
            if not node.left and not node.right and node.red:
                return 0, False

            # if node is red, check children are black
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            # descend tree and check black counts are balanced
            if node.left and node.right:

                # check children's parents are correct
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                # check children's counts are ok
                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red




def write_tree_as_dot(t, f, show_nil=False):
    "Write the tree in the dot language format to f."
    def node_id(node):
        return 'N%d' % id(node)

    def node_color(node):
        if node.red:
            return "red"
        else:
            return "black"

    def visit_node(node):
        "Visit a node."
        print >> f, "  %s [label=\"%s\", color=\"%s\"];" % (node_id(node), node, node_color(node))
        if node.left:
            if node.left != t.nil or show_nil:
                visit_node(node.left)
                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.left))
        if node.right:
            if node.right != t.nil or show_nil:
                visit_node(node.right)
                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.right))

    print >> f, "// Created by rbtree.write_dot()"
    print >> f, "digraph red_black_tree {"
    visit_node(t.root)
    print >> f, "}"


def delete_tree(t, key):
    #assert t.check_invariants()
    t.delete_key(key)
    #assert t.check_invariants()

def insert_tree(t, key):
    "Insert keys one by one checking invariants and membership as we go."
    assert t.check_invariants()
    #for i, key in enumerate(keys):
    #    for key2 in keys[:i]:
    #        assert t.nil != t.search(key2)
    #    for key2 in keys[i:]:
    #        assert (t.nil == t.search(key2)) ^ (key2 in keys[:i])
    #    t.insert_key(key)
    t.insert_key(key)
    assert t.check_invariants()


if '__main__' == __name__:
    import os, sys
    os.system('rm ../Results/Dot/*.*')
    os.system('rm ../Results/Svg/*.*')
    def write_tree(t, filename):
        "Write the tree as an SVG file."
        f = open('../Results/Dot/%s.dot' % filename, 'w')
        write_tree_as_dot(t, f)
        f.close()
        os.system('dot ../Results/Dot/%s.dot -Tsvg -o ../Results/Svg/%s.svg' % (filename, filename))

    # test the rbtree
    t = rbtree()
    i = 0
    while True:
        i += 1
        print "MENU : 1.Insert 2.Delete 3.Search \n(Press any other number to Exit!)"
        choice = input("Enter your choice : ")
        if choice == 1:
            key = input("Enter key : ")
            insert_tree(t, key)
            write_tree(t, 'tree-'+str(i)+'-inserting-'+str(key))
        elif choice == 2:
            key = input("Enter key : ")
            delete_tree(t, key)
            write_tree(t, 'tree-'+str(i)+'-deleting-'+str(key))
        elif choice == 3:
            key = input("Enter key : ")
            assert (t.nil != t.search(key)), "Key not found!"
            print "Key is present in the tree!"
        else:
            sys.exit("Exiting!")
