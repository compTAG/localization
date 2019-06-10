import readLas
import PCPDS as section

def main():
    # Temp test for pcpds
    test = section.PCPDS(1,1,1)
    test.save()
    
    temp = section.load_section(1,1,1)
    
    # temp now has the ability to call methods from the PCPDS object that has been loaded

if __name__ == '__main__':
    main()
