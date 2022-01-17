from random import randint
from models import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

nums={
    'one':1,
    'two':2,
    'three':3,
    'four':4,
    'five':5,
    'six':6,
    'seven':7,
    'eight':8,
    'nine':9    }

strat=((0,'X','X'),('X',0,'X'),('X','X',0))

win_strat=((0,'O','O'),('O',0,'O'),('O','O',0))

diag = {
    '60':1,
    '61':5,
    '62':9,
    '70':3,
    '71':5,
    '72':7}

class SinglePlayer:
    def __init__(self, a1=0, a2=0, a3=0, b1=0, b2=0, b3=0, c1=0, c2=0, c3=0):
        self.a1=a1
        self.a2=a2
        self.a3=a3
        
        self.b1=b1
        self.b2=b2
        self.b3=b3
        
        self.c1=c1
        self.c2=c2
        self.c3=c3

    def to_list(self):
        a=list(map(str, [self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3]))
        return a

    def validate(self):
        self.all_items = [self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3]
        if self.all_items.count(0)>5:
            return False

        self.row1=(self.a1,self.a2,self.a3)
        self.row2=(self.b1,self.b2,self.b3)
        self.row3=(self.c1,self.c2,self.c3)

        self.col1=(self.a1,self.b1,self.c1)
        self.col2=(self.a2,self.b2,self.c2)
        self.col3=(self.a3,self.b3,self.c3)

        self.diagonalf=(self.a3,self.b2,self.c1)
        self.diagonalb=(self.a1,self.b2,self.c3)

        self.diagonals=(self.diagonalb,self.diagonalf)

        self.horizontal=(self.row1,self.row2,self.row3)
        self.vertical=(self.col1,self.col2,self.col3)

        self.all=(self.horizontal, self.vertical, self.diagonals)

        for item in self.all:
            for line in item:
                if 0 in line:
                  cont = True
                elif line[0]==line[1]==line[2]:
                    if line[0]=='O':
                      cont = False
                      return 'Lose'
                    return True
            if self.all_items.count(0)==1 and cont==True:
                index=self.all_items.index(0)
                self.entry(index+1, 'X')
                self.row1=(self.a1,self.a2,self.a3)
                self.row2=(self.b1,self.b2,self.b3)
                self.row3=(self.c1,self.c2,self.c3)

                self.col1=(self.a1,self.b1,self.c1)
                self.col2=(self.a2,self.b2,self.c2)
                self.col3=(self.a3,self.b3,self.c3)

                self.diagonalf=(self.a3,self.b2,self.c1)
                self.diagonalb=(self.a1,self.b2,self.c3)

                self.diagonals=(self.diagonalb,self.diagonalf)

                self.horizontal=(self.row1,self.row2,self.row3)
                self.vertical=(self.col1,self.col2,self.col3)

                self.all=(self.horizontal, self.vertical, self.diagonals)
                for item in self.all:
                    for line in item:
                        if line[0]==line[1]==line[2]:
                            if line[0]=='O':
                                return 'Lose'
                            return True
                return 'Draw'

        return False

    def entry(self, n, entry):
        if n==1:
            self.a1=entry
        elif n==2:
            self.a2=entry
        elif n==3:
            self.a3=entry
        elif n==4:
            self.b1=entry
        elif n==5:
            self.b2=entry
        elif n==6:
            self.b3=entry
        elif n==7:
            self.c1=entry
        elif n==8:
            self.c2=entry
        elif n==9:
            self.c3=entry
        
    def ai_move(self):
        #not a good A.I.
        self.all_items = [self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3]
        if self.all_items.count('X')>1:
            self.row1=(self.a1,self.a2,self.a3)
            self.row2=(self.b1,self.b2,self.b3)
            self.row3=(self.c1,self.c2,self.c3)

            self.col1=(self.a1,self.b1,self.c1)
            self.col2=(self.a2,self.b2,self.c2)
            self.col3=(self.a3,self.b3,self.c3)

            self.diagonalf=(self.a3,self.b2,self.c1)
            self.diagonalb=(self.a1,self.b2,self.c3)

            self.all3 = [self.row1,self.row2,self.row3,self.col1,self.col2,self.col3,self.diagonalb,self.diagonalf]

            for r in range(0,8):
                if self.all3[r] in win_strat:
                    j = win_strat.index(self.all3[r])
                    if r<3:
                        a=3*r
                        n = 1+j+a
                        self.entry(n,'O')
                        return
                    elif r>2 and r<6:
                        a = 3*j
                        n = r+a-2
                        self.entry(n,'O')
                        return
                    elif r>5 and r<8:
                        n=diag[str(r)+str(j)]
                        self.entry(n,'O')
                        return
            
            for r in range(0,8):
                if self.all3[r] in strat:
                    j = strat.index(self.all3[r])
                    if r<3:
                        a=3*r
                        n = 1+j+a
                        self.entry(n,'O')
                        return
                    elif r>2 and r<6:
                        a = 3*j
                        n = r+a-2
                        self.entry(n,'O')
                        return
                    elif r>5 and r<8:
                        n=diag[str(r)+str(j)]
                        self.entry(n,'O')
                        return
            a=True
            if self.all_items[4]==0:
                self.entry(5,'O')
                return
            while a:
                n = randint(1, 9)
                if self.all_items[n-1]==0:
                    self.entry(n, 'O')
                    a=False
                    return
                        
        else:
            a=True
            if self.all_items[4]==0:
                self.entry(5,'O')
                return
            while a:
                n = randint(1, 9)
                if self.all_items[n-1]==0:
                    self.entry(n, 'O')
                    a=False
                    return

    def __repr__(self):
        # for making string that will be added to database
        return' '.join(self.to_list())
    
    @classmethod
    def from_string(cls, str: str):
        lst=str.split(' ')
        for i in range(9):
            if lst[i]=='0':
                lst[i]=0
        return SinglePlayer(*lst)

    @classmethod
    def new(cls, id, name):
        brd = str(SinglePlayer())
        session.add(PrivateBoards(id = id, board = brd, user_name = name))
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
    
    @classmethod
    def newGame(cls, id, name:str):
        brd = str(SinglePlayer())
        a = session.query(PrivateBoards).filter(PrivateBoards.id == id)
        if a.first():
            a.update({PrivateBoards.board : brd})
            try:
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False
        else:
            cls.new(id, name)
            return False

    @classmethod
    def getBoard(cls, id):
        user = session.query(PrivateBoards).filter(PrivateBoards.id == id).first()
        if user:
            return cls.from_string(user.board)
    
    def modify(self, id):
        brd=self.__repr__()
        try:
            session.query(PrivateBoards).filter(PrivateBoards.id == id).update({"board":brd})
            try:
                session.commit()
                return True
            except Exception:
                session.rollback()
        except Exception:
            return False

    @classmethod
    def win(cls, id):
        session.query(PrivateBoards).filter(PrivateBoards.id == id).update({PrivateBoards.games:(PrivateBoards.games+1), PrivateBoards.win:(PrivateBoards.win+1)})
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def lose(cls, id):
        session.query(PrivateBoards).filter(PrivateBoards.id == id).update({PrivateBoards.games:(PrivateBoards.games+1), PrivateBoards.lose:(PrivateBoards.lose+1)})
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def tie(cls, id):
        session.query(PrivateBoards).filter(PrivateBoards.id == id).update({PrivateBoards.games:(PrivateBoards.games+1), PrivateBoards.tie:(PrivateBoards.tie+1)})
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def stats(cls, id):
        user = session.query(PrivateBoards).filter(PrivateBoards.id == id).first()
        if user:
            stat={  "games":user.games,
                    "win":user.win,
                    "tie":user.tie,
                    "lose":user.lose    }
            return stat

    def inputMarkup(self, no_input=False):
        markup = InlineKeyboardMarkup(row_width = 3)
        items = self.to_list()
        btns = []
        for i in range(9):
            if items[i]==0 or items[i]=='0':
                btns.append(InlineKeyboardButton('_'))
                if no_input:
                    btns[i].callback_data='pass'
                else:
                    btns[i].callback_data=(i+1)
            elif items[i]=='X':
                btns.append(InlineKeyboardButton('X', callback_data='pass'))
            elif items[i]=='O':
                btns.append(InlineKeyboardButton('O', callback_data='pass'))
        markup.add(*btns)
        return markup


class MultiPlayer:
    def __init__(self, a1=0, a2=0, a3=0, b1=0, b2=0, b3=0, c1=0, c2=0, c3=0):
        self.a1=a1
        self.a2=a2
        self.a3=a3
        
        self.b1=b1
        self.b2=b2
        self.b3=b3
        
        self.c1=c1
        self.c2=c2
        self.c3=c3
    
    def to_list(self):
        a=list(map(str, [self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3]))
        return a
    
    def validate(self):
        self.all_items = [self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, self.c1, self.c2, self.c3]
        if self.all_items.count(0)>5:
            return False

        self.row1=(self.a1,self.a2,self.a3)
        self.row2=(self.b1,self.b2,self.b3)
        self.row3=(self.c1,self.c2,self.c3)

        self.col1=(self.a1,self.b1,self.c1)
        self.col2=(self.a2,self.b2,self.c2)
        self.col3=(self.a3,self.b3,self.c3)

        self.diagonalf=(self.a3,self.b2,self.c1)
        self.diagonalb=(self.a1,self.b2,self.c3)

        self.diagonals=(self.diagonalb,self.diagonalf)

        self.horizontal=(self.row1,self.row2,self.row3)
        self.vertical=(self.col1,self.col2,self.col3)

        self.all=(self.horizontal, self.vertical, self.diagonals)

        for item in self.all:
            for line in item:
                if 0 in line:
                  cont = True
                elif line[0]==line[1]==line[2]:
                    if line[0]=='O':
                      cont = False
                      return 'Player 2'
                    return 'Player 1'
            if self.all_items.count(0)==1 and cont==True:
                index=self.all_items.index(0)
                self.entry(index+1, 'X')
                self.row1=(self.a1,self.a2,self.a3)
                self.row2=(self.b1,self.b2,self.b3)
                self.row3=(self.c1,self.c2,self.c3)

                self.col1=(self.a1,self.b1,self.c1)
                self.col2=(self.a2,self.b2,self.c2)
                self.col3=(self.a3,self.b3,self.c3)

                self.diagonalf=(self.a3,self.b2,self.c1)
                self.diagonalb=(self.a1,self.b2,self.c3)

                self.diagonals=(self.diagonalb,self.diagonalf)

                self.horizontal=(self.row1,self.row2,self.row3)
                self.vertical=(self.col1,self.col2,self.col3)

                self.all=(self.horizontal, self.vertical, self.diagonals)
                for item in self.all:
                    for line in item:
                        if line[0]==line[1]==line[2]:
                            if line[0]=='O':
                                return 'Player 2'
                            return 'Player 1'
                return 'Draw'
        return False

    def entry(self, n, entry):
        if n==1:
            self.a1=entry
        elif n==2:
            self.a2=entry
        elif n==3:
            self.a3=entry
        elif n==4:
            self.b1=entry
        elif n==5:
            self.b2=entry
        elif n==6:
            self.b3=entry
        elif n==7:
            self.c1=entry
        elif n==8:
            self.c2=entry
        elif n==9:
            self.c3=entry

    def __repr__(self):
        # for making string that will be added to database
        return' '.join(self.to_list())
    
    @classmethod
    def from_string(cls, str: str):
        lst=str.board.split(' ')
        for i in range(9):
            if lst[i]=='0':
                lst[i]=0
        return MultiPlayer(*lst)

    @classmethod
    def newGroup(cls, id : str):
        brd = str(MultiPlayer())
        session.add(GroupBoards(id=id, board=brd))
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def newGame(cls, id :str):
        cls.gameEnd(id)
        brd = str(MultiPlayer())
        a = session.query(GroupBoards).filter(GroupBoards.id == id)
        if a.first():
            a.update({GroupBoards.board : brd})
            try:
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False
        else:
            cls.newGroup(id)
            return False
    
    @classmethod
    def getBoard(cls, id : str) :
        grp = session.query(GroupBoards).filter(GroupBoards.id == id).first()
        if grp:
            return MultiPlayer.from_string(grp.board)

    def modify(cls, id:str):
        brd=cls.__repr__()
        try:
            session.query(MultiPlayer).filter(MultiPlayer.id == id).update({"board":brd})
            try:
                session.commit()
                return True
            except Exception:
                session.rollback()
        except Exception:
            return False

    @classmethod
    def gameEnd(cls, id):
        session.query(GroupBoards).filter(GroupBoards.id == id).update({GroupBoards.player1 : None, GroupBoards.player2 : None})
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def addPlayer1(cls, id : str, player):
        session.query(GroupBoards).filter(GroupBoards.id == id).update({GroupBoards.player1 : player})
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def addPlayer2(cls, id : str, player):
        session.query(GroupBoards).filter(GroupBoards.id == id).update({GroupBoards.player2 : player})
        try:
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def currPlayers(cls, id):
        grp = session.query(GroupBoards).filter(GroupBoards.id == id).first()
        if grp:
            return [grp.player1, grp.player2]

    def inputMarkup(self):
        markup = InlineKeyboardMarkup(row_width = 3)
        items = self.to_list()
        btns = []
        for i in range(9):
            if items[i]==0 or items[i]=='0':
                btns.append(InlineKeyboardButton('_', callback_data=(i+1)))
            elif items[i]=='X':
                btns.append(InlineKeyboardButton('X', callback_data='pass'))
            elif items[i]=='O':
                btns.append(InlineKeyboardButton('O', callback_data='pass'))
        markup.add(*btns)
        return markup
    