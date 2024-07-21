from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///saskaitos_bankuose.db")
Base = declarative_base()



class Asmuo(Base):
    __tablename__ = "asmuo"
    id = Column(Integer, primary_key=True)
    vardas = Column("Vardas", String)
    pavarde = Column("Pavardė", String)
    asmens_kodas = Column(Integer)
    tel_numeris = Column(Integer)
    bankai = relationship("Bankas", back_populates="asmuo")
    saskaitos = relationship("Saskaita", back_populates="asmuo")

class Bankas(Base):
    __tablename__ = "bankas"
    id = Column(Integer, primary_key=True)
    pavadinimas = Column("Pavadinimas", String)
    adresas = Column("Adresas", String)
    banko_kodas = Column("Banko_kodas", String)
    swift = Column("SWIFT", String)
    asmuo_id = Column(Integer, ForeignKey("asmuo.id"))
    asmuo = relationship("Asmuo", back_populates="bankai")
    saskaitos = relationship("Saskaita", back_populates="bankas")

class Saskaita(Base):
    __tablename__ = "saskaita"
    id = Column(Integer, primary_key=True)
    numeris = Column("Numeris", String)
    balansas = Column("Balansas", String)
    asmuo_id = Column(Integer, ForeignKey("asmuo.id"))
    asmuo = relationship("Asmuo", back_populates="saskaitos")
    bankas_id = Column(Integer, ForeignKey("bankas.id"))
    bankas = relationship("Bankas", back_populates="saskaitos")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

asmuo = Asmuo(vardas="Vardenis", pavarde="Pavardenis", asmens_kodas="30000000000", tel_numeris="860000000")
asmuo2 = Asmuo(vardas="Vardaitis", pavarde="Pavardaitis", asmens_kodas="30000000001", tel_numeris="860000001")
bankas = Bankas(pavadinimas="Bankas", adresas="Banko 1", banko_kodas="111", swift="1111")
bankas2 = Bankas(pavadinimas="Bank", adresas="Bank 12", banko_kodas="121", swift="1121")
saskaita = Saskaita(numeris="01", balansas="10000")
saskaita2 = Saskaita(numeris="02", balansas="9000")


asmuo.bankai.append(bankas)
asmuo.bankai.append(bankas2)
asmuo.saskaitos.append(saskaita)
asmuo.saskaitos.append(saskaita2)
bankas.saskaitos.append(saskaita)
bankas.saskaitos.append(saskaita2)
session.add(bankas)
session.add(asmuo)
session.commit()


#pamokos pvz
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
engine = create_engine('sqlite:///bankas.db')
Base = declarative_base()
class Asmuo(Base):
    __tablename__ = 'asmuo'
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    pavarde = Column(String)
    asmens_kodas = Column(String, unique=True)
    tel_numeris = Column(String)
    saskaitos = relationship('Saskaita', back_populates='asmuo')
class Bankas(Base):
    __tablename__ = 'bankas'
    id = Column(Integer, primary_key=True)
    pavadinimas = Column(String)
    adresas = Column(String)
    banko_kodas = Column(String)
    swift_kodas = Column(String)
    saskaitos = relationship('Saskaita', back_populates='bankas')
class Saskaita(Base):
    __tablename__ = 'saskaita'
    id = Column(Integer, primary_key=True)
    numeris = Column(String)
    balansas = Column(Integer)
    asmens_id = Column(Integer, ForeignKey('asmuo.id'))
    banko_id = Column(Integer, ForeignKey('bankas.id'))
    asmuo = relationship('Asmuo', back_populates='saskaitos')
    bankas = relationship('Bankas', back_populates='saskaitos')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
def grazinti_asmens_kodo_kontrolini(asmens_kodas):
    kodas = str(asmens_kodas)
    A = int(kodas[0])
    B = int(kodas[1])
    C = int(kodas[2])
    D = int(kodas[3])
    E = int(kodas[4])
    F = int(kodas[5])
    G = int(kodas[6])
    H = int(kodas[7])
    I = int(kodas[8])
    J = int(kodas[9])
    S = A * 1 + B * 2 + C * 3 + D * 4 + E * 5 + F * 6 + G * 7 + H * 8 + I * 9 + J * 1
    if S % 11 != 10:
        kontrolinis = S % 11
    else:
        S = A * 3 + B * 4 + C * 5 + D * 6 + E * 7 + F * 8 + G * 9 + H * 1 + I * 2 + J * 3
        if S % 11 != 10:
            kontrolinis = S % 11
        else:
            kontrolinis = 0
    return kontrolinis
def is_valid_asmens_kodas(asmens_kodas):
    paskutinis_sk = int(str(asmens_kodas)[-1])
    return paskutinis_sk == grazinti_asmens_kodo_kontrolini(asmens_kodas)
def sukurti_nauja_asmeni():
    print("Naujo asmens kūrimas:")
    vardas = input("Vardas: ")
    pavarde = input("Pavardė: ")
    tel_numeris = input("Telefono numeris: ")
    asmens_kodas = input("Asmens kodas: ")
    if asmens_kodas.isdigit() and len(asmens_kodas) != 11:
        print("Asmens kodas neteisingas.")
    else:
        existing_asmuo = session.query(Asmuo).filter_by(asmens_kodas=asmens_kodas).first()
        if existing_asmuo:
            print("Toks asmuo jau yra įrašytas:")
            print(f"Vardas: {existing_asmuo.vardas}, Pavardė: {existing_asmuo.pavarde}, Asmens kodas: {existing_asmuo.asmens_kodas}, Telefono numeris: {existing_asmuo.tel_numeris}")
        else:
            if is_valid_asmens_kodas(asmens_kodas):
                naujas_asmuo = Asmuo(vardas=vardas, pavarde=pavarde, asmens_kodas=asmens_kodas, tel_numeris=tel_numeris)
                session.add(naujas_asmuo)
                session.commit()
                print("Asmuo sukurtas sėkmingai. Spauskite Enter, kad grįžti į pagrindinį meniu.")
            else:
                print("Asmens kodas neteisingas.")
def sukurti_nauja_banka():
    print("Naujo banko kūrimas:")
    pavadinimas = input("Pavadinimas: ")
    adresas = input("Adresas: ")
    banko_kodas = input("Banko kodas: ")
    swift_kodas = input("SWIFT kodas: ")
    naujas_bankas = Bankas(pavadinimas=pavadinimas, adresas=adresas, banko_kodas=banko_kodas, swift_kodas=swift_kodas)
    session.add(naujas_bankas)
    session.commit()
    print("Bankas sukurtas sėkmingai. Spauskite Enter, kad grįžti į pagrindinį meniu.")
def sukurti_nauja_saskaita():
    print("Naujos sąskaitos kūrimas:")
    numeris = input("Sąskaitos numeris: ")
    perziureti_visus_vartotojus()
    asmens_id = int(input("Įveskite asmens ID (priskirti asmeniui): "))
    perziureti_visus_bankus()
    banko_id = int(input("Įveskite banko ID (priskirti bankui): "))
    asmuo = session.query(Asmuo).filter_by(id=asmens_id).first()
    bankas = session.query(Bankas).filter_by(id=banko_id).first()
    if asmuo and bankas:
        nauja_saskaita = Saskaita(numeris=numeris, asmuo=asmuo, bankas=bankas)
        session.add(nauja_saskaita)
        session.commit()
        print("Nauja sąskaita sėkmingai sukurta!")
    else:
        print("Nepavyko rasti atitinkamo asmens arba banko.")
    input("Spauskite Enter, kad grįžti į pradinį meniu.")
def perziureti_saskaitas():
    visi_saskaitos = session.query(Saskaita).all()
    if not visi_saskaitos:
        print("Nėra sąskaitų.")
    else:
        print("Sąskaitų sąrašas:")
        for x in visi_saskaitos:
            print(
                f"ID: {x.id}, Numeris: {x.numeris}, Balansas: {x.balansas}, Asmuo: {x.asmuo.vardas} {x.asmuo.pavarde}, Bankas: {x.bankas.pavadinimas}")
    input("Spauskite Enter, kad grįžti į pagrindinį meniu.")
def prideti_pinigus_i_saskaita():
    print("Pridėti pinigus į sąskaitą")
    perziureti_visus_vartotojus()
    asmens_id = int(input("Įveskite vartotojo ID: "))
    asmens_saskaitos = session.query(Saskaita).filter_by(asmens_id=asmens_id).all()
    if not asmens_saskaitos:
        print(f"Šis asmuo neturi sąskaitų.")
        return
    print("Pasirinkite sąskaitą, į kurią norite pridėti pinigus:")
    for saskaita in asmens_saskaitos:
        print(f"ID: {saskaita.id}, Numeris: {saskaita.numeris}, Balansas: {saskaita.balansas}")
    saskaitos_id = int(input("Įveskite ID sąskaitos: "))
    saskaita = session.query(Saskaita).filter_by(id=saskaitos_id, asmens_id=asmens_id).first()
    if saskaita:
        suma = float(input("Įveskite sumą, kurią norite pridėti: "))
        dabartinis_balansas = saskaita.balansas
        if dabartinis_balansas is not None:
            naujas_balansas = dabartinis_balansas + suma
        else:
            naujas_balansas = suma
        saskaita.balansas = naujas_balansas
        session.commit()
        print(f"Pridėta {suma}. Dabartinis balansas sąskaitoje su ID {saskaitos_id}: {naujas_balansas}")
    else:
        print(f"Sąskaita su ID {saskaitos_id} nerasta.")
    input("Spauskite Enter, kad grįžti į pagrindinį meniu.")
def nuimti_pinigus_is_saskaita():
    print("Nuimti pinigus iš sąskaitos")
    perziureti_visus_vartotojus()
    asmens_id = int(input("Iveskite vartotojo ID: "))
    asmens_saskaitos = session.query(Saskaita).filter_by(asmens_id=asmens_id).all()
    if not asmens_saskaitos:
        print(f"Šis asmuo neturi sąskaitų.")
        return
    print("Pasirinkite sąskaitą, iš kurios norite nuimti pinigus:")
    for saskaita in asmens_saskaitos:
        print(f"ID: {saskaita.id}, Numeris: {saskaita.numeris}, Balansas: {saskaita.balansas}")
    saskaitos_id = int(input("Įveskite ID sąskaitos: "))
    saskaita = session.query(Saskaita).filter_by(id=saskaitos_id, asmens_id=asmens_id).first()
    if saskaita:
        suma = float(input("Įveskite sumą, kurią norite nuimti: "))
        dabartinis_balansas = saskaita.balansas
        if dabartinis_balansas is not None and dabartinis_balansas >= suma:
            naujas_balansas = dabartinis_balansas - suma
            saskaita.balansas = naujas_balansas
            session.commit()
            print(f"Nuimta {suma}. Dabartinis balansas sąskaitoje su ID {saskaitos_id}: {naujas_balansas}")
        else:
            print("Nepakankamai lėšų sąskaitoje.")
    else:
        print(f"Sąskaita su ID {saskaitos_id} nerasta.")
    input("Spauskite Enter, kad grįžti į pagrindinį meniu.")
def perziureti_visus_bankus():
    bankai = session.query(Bankas).all()
    if not bankai:
        print("Nėra banku.")
    else:
        print("Banku sąrašas:")
        for bankas in bankai:
            print(f"ID: {bankas.id}, Banko pavadinimas: {bankas.pavadinimas}, Adresas: {bankas.adresas}, Banko kodas: {bankas.banko_kodas}, SWIFT kodas: {bankas.swift_kodas}")
def perziureti_visus_vartotojus():
    vartotojai = session.query(Asmuo).all()
    if not vartotojai:
        print("Nėra vartotoju.")
    else:
        print("Vartotoju sąrašas:")
        for vartotojas in vartotojai:
            print(f"ID: {vartotojas.id}, Vardas: {vartotojas.vardas}, Pavardė: {vartotojas.pavarde}, Asmens kodas: {vartotojas.asmens_kodas}, Tel. numeris: {vartotojas.tel_numeris}")
while True:
    print("Pasirinkite veiksmą:")
    print("1. Sukurti naują asmenį")
    print("2. Sukurti naują banką")
    print("3. Sukurti naują sąskaitą")
    print("4. Peržiūrėti sąskaitas")
    print("5. Pridėti pinigus į sąskaitą")
    print("6. Nuimti pinigus iš sąskaitos")
    print("7. Peržiūrėti visus bankus")
    print("8. Peržiūrėti visus vartotojus")
    print("9. Išeiti")
    choice = input("Jūsų pasirinkimas: ")
    if choice == '1':
        sukurti_nauja_asmeni()
    elif choice == '2':
        sukurti_nauja_banka()
    elif choice == '3':
        sukurti_nauja_saskaita()
    elif choice == '4':
        perziureti_saskaitas()
    elif choice == '5':
        prideti_pinigus_i_saskaita()
    elif choice == '6':
        nuimti_pinigus_is_saskaita()
    elif choice == '7':
        perziureti_visus_bankus()
        input("Spauskite Enter, kad grįžti į pagrindinį meniu.")
    elif choice == '8':
        perziureti_visus_vartotojus()
        input("Spauskite Enter, kad grįžti į pagrindinį meniu.")
    elif choice == '9':
        print("Programa baigta.")
        break
    else:
        print("Neatpažintas pasirinkimas. Bandykite dar kartą.")
